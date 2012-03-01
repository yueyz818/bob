/**
 * @file cxx/io/src/HDF5Group.cc
 * @author Andre Anjos <andre.anjos@idiap.ch>
 * @date Wed 29 Feb 17:24:10 2012 
 *
 * @brief Implements HDF5 groups.
 *
 * Copyright (C) 2011-2012 Idiap Research Institute, Martigny, Switzerland
 * 
 * This program is free software: you can redistribute it and/or modify
 * it under the terms of the GNU General Public License as published by
 * the Free Software Foundation, version 3 of the License.
 * 
 * This program is distributed in the hope that it will be useful,
 * but WITHOUT ANY WARRANTY; without even the implied warranty of
 * MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
 * GNU General Public License for more details.
 * 
 * You should have received a copy of the GNU General Public License
 * along with this program.  If not, see <http://www.gnu.org/licenses/>.
 */

#include <boost/make_shared.hpp>
#include <boost/filesystem.hpp>
#include <boost/format.hpp>
#include <boost/algorithm/string.hpp>
#include "io/HDF5Group.h"
#include "io/HDF5Utils.h"
#include "core/logging.h"

namespace h5 = bob::io::detail::hdf5;
namespace io = bob::io;

/**
 * Creates an "auto-destructible" HDF5 Group
 */
static void delete_h5g (hid_t* p) {
  if (*p >= 0) {
    H5Gclose(*p);
  }
  delete p;
  p=0; 
}

static boost::shared_ptr<hid_t> create_new_group(boost::shared_ptr<hid_t> p,
    const std::string& name) {
  boost::shared_ptr<hid_t> retval(new hid_t(-1), std::ptr_fun(delete_h5g));
  *retval = H5Gcreate(*p, name.c_str(), H5P_DEFAULT, H5P_DEFAULT, H5P_DEFAULT); 
  if (*retval < 0) throw io::HDF5StatusError("H5Gcreate", *retval);
  return retval;
}

static boost::shared_ptr<hid_t> open_group(boost::shared_ptr<hid_t> g,
    const char* name) {
  boost::shared_ptr<hid_t> retval(new hid_t(-1), std::ptr_fun(delete_h5g));
  *retval = H5Gopen(*g, name, H5P_DEFAULT); 
  if (*retval < 0) throw io::HDF5StatusError("H5Gopen", *retval);
  return retval;
}

h5::Group::Group(boost::shared_ptr<h5::Group> parent, const std::string& name): 
  m_name(name),
  m_id(create_new_group(parent->location(), name)),
  m_parent(parent)
{
}

/**
 * Simple wrapper to call internal h5::Group::iterate_callback, that can call
 * Group and Dataset constructors. Note that those are private or protected for
 * design reasons.
 */ 
static herr_t group_iterate_callback(hid_t self, const char *name, 
    const H5L_info_t *info, void *object) {
  return static_cast<h5::Group*>(object)->iterate_callback(self, name, info);
}

herr_t h5::Group::iterate_callback(hid_t self, const char *name, 
    const H5L_info_t *info) {

  // If we are not looking at a hard link to the data, just ignore
  if (info->type != H5L_TYPE_HARD) {
    TDEBUG1("Ignoring soft-link `" << name << "' in HDF5 file");
    return 0;
  }

  // Get information about the HDF5 object
  H5O_info_t obj_info;
  herr_t status = H5Oget_info_by_name(self, name, &obj_info, H5P_DEFAULT);
  if (status < 0) throw io::HDF5StatusError("H5Oget_info_by_name", status);

  switch(obj_info.type) {
    case H5O_TYPE_GROUP:
      //creates with recursion
      m_groups[name] = boost::make_shared<h5::Group>(shared_from_this(), 
          name, true);
      m_groups[name]->open_recursively();
      break;
    case H5O_TYPE_DATASET:
      m_datasets[name] = boost::make_shared<h5::Dataset>(shared_from_this(), 
          std::string(name));
      break;
    default:
      break;
  }

  return 0;
}

h5::Group::Group(boost::shared_ptr<h5::Group> parent,
    const std::string& name, bool):
  m_name(name),
  m_id(open_group(parent->location(), name.c_str())),
  m_parent(parent)
{
  //checks name
  if (!m_name.size() || m_name == "." || m_name == "..") {
    boost::format m("Cannot create group with illegal name `%s' at `%s:%s'");
    m % name % file()->filename() % path();
    throw std::runtime_error(m.str().c_str());
  }
}

void h5::Group::open_recursively() {
  //iterates over this group only and instantiates what needs to be instantiated
  herr_t status = H5Literate(*m_id, H5_INDEX_NAME,
      H5_ITER_NATIVE, 0, group_iterate_callback, static_cast<void*>(this));
  if (status < 0) throw io::HDF5StatusError("H5Literate", status);
}

h5::Group::Group(boost::shared_ptr<h5::File> parent):
  m_name(""),
  m_id(open_group(parent->location(), "/")),
  m_parent()
{
}

h5::Group::~Group() { }

const boost::shared_ptr<h5::Group> h5::Group::parent() const {
  return m_parent.lock();
}

boost::shared_ptr<h5::Group> h5::Group::parent() {
  return m_parent.lock();
}

const std::string& h5::Group::filename() const {
  return parent()->filename();
}

std::string h5::Group::path() const {
  return (m_name.size()?parent()->path():"") + "/" + m_name;
}

const boost::shared_ptr<h5::File> h5::Group::file() const {
  return parent()->file();
}

boost::shared_ptr<h5::File> h5::Group::file() {
  return parent()->file();
}

boost::shared_ptr<h5::Group> h5::Group::cd(const std::string& dir) {
  //empty dir == void action, return self
  if (!dir.size()) return shared_from_this();
  
  if (dir[0] == '/') { //absolute path given, apply to root node
    return file()->root()->cd(dir.substr(1));
  }

  //relative path given, start from self
  std::string::size_type pos = dir.find_first_of('/');
  if (pos == std::string::npos) { //it should be one of my children
    if (dir == ".") return shared_from_this();
    if (dir == "..") {
      if (!m_name.size()) { //this is the root group already
        boost::format m("Cannot go beyond root directory at file `%s'");
        m % file()->filename();
        throw std::runtime_error(m.str().c_str());
      }
      //else, just return its parent
      return parent();
    }
    if (!has_group(dir)) {
      boost::format m("Cannot find group `%s' at `%s:%s'");
      m % dir % file()->filename() % path();
      throw std::runtime_error(m.str().c_str());
    }
    //else, just return the named group
    return m_groups[dir];
  }

  //if you get to this point, we are just traversing
  std::string mydir = dir.substr(0, pos);
  if (mydir == ".") return cd(dir.substr(pos+1));
  if (mydir == "..") return parent()->cd(dir.substr(pos+1));
  if (!has_group(mydir)) {
    boost::format m("Cannot find group `%s' at `%s:%s'");
    m % dir % file()->filename() % path();
    throw std::runtime_error(m.str().c_str());
  }

  //else, just recurse to the next group
  return m_groups[mydir]->cd(dir.substr(pos+1));
}

const boost::shared_ptr<h5::Group> h5::Group::cd(const std::string& dir) const {
  return const_cast<h5::Group*>(this)->cd(dir);
}

boost::shared_ptr<h5::Dataset> h5::Group::operator[] (const std::string& dir) {
  std::string::size_type pos = dir.find_last_of('/');
  if (pos == std::string::npos) { //search on the current group
    if (!has_dataset(dir)) {
      boost::format m("Cannot find dataset `%s' at `%s:%s'");
      m % dir % file()->filename() % path();
      throw std::runtime_error(m.str().c_str());
    }
    return m_datasets[dir];
  }

  //if you get to this point, the search routine needs to be performed on
  //another group, indicated by the path. So, we first cd() there and then do
  //the same as we do here. This will recurse through the directory structure
  //until we find the place defined by the user or raise an exception.
  std::string dest = dir.substr(0, pos);
  if (!dest.size()) dest = "/";
  boost::shared_ptr<h5::Group> g = cd(dest);
  return g->operator[](dir.substr(pos+1));
}

const boost::shared_ptr<h5::Dataset> h5::Group::operator[] (const std::string& dir) const {
  return const_cast<h5::Group*>(this)->operator[](dir);
}

void h5::Group::reset() {
  typedef std::map<std::string, boost::shared_ptr<h5::Group> > group_map_type;
  for (group_map_type::const_iterator it = m_groups.begin();
      it != m_groups.end(); ++it) {
    remove_group(it->first);
  }

  typedef std::map<std::string, boost::shared_ptr<h5::Dataset> > 
    dataset_map_type;
  for (dataset_map_type::const_iterator it = m_datasets.begin();
      it != m_datasets.end(); ++it) {
    remove_dataset(it->first);
  }
}

boost::shared_ptr<h5::Group> h5::Group::create_group(const std::string& dir) {
  std::string::size_type pos = dir.find_last_of('/');
  if (pos == std::string::npos) { //creates on the current group
    boost::shared_ptr<h5::Group> g =
      boost::make_shared<h5::Group>(shared_from_this(), dir);
    m_groups[dir] = g;
    return g;
  }

  //if you get to this point, the search routine needs to be performed on
  //another group, indicated by the path. So, we first cd() there and then do
  //the same as we do here. This will recurse through the directory structure
  //until we find the place defined by the user or raise an exception.
  std::string dest = dir.substr(0, pos);
  if (!dest.size()) dest = "/";
  boost::shared_ptr<h5::Group> g = cd(dest);
  return g->create_group(dir.substr(pos+1));
}

void h5::Group::remove_group(const std::string& dir) {
  std::string::size_type pos = dir.find_last_of('/');
  if (pos == std::string::npos) { //copy on the current group
    herr_t status = H5Ldelete(*m_id, dir.c_str(), H5P_DEFAULT);
    if (status < 0) throw io::HDF5StatusError("H5Ldelete", status);
    typedef std::map<std::string, boost::shared_ptr<h5::Group> > map_type;
    map_type::iterator it = m_groups.find(dir);
    m_groups.erase(it);
    return;
  }

  //if you get to this point, the removal routine needs to be performed on
  //another group, indicated by the path. So, we first cd() there and then do
  //the same as we do here. This will recurse through the directory structure
  //until we find the place defined by the user or raise an exception.
  std::string dest = dir.substr(0, pos);
  if (!dest.size()) dest = "/";
  boost::shared_ptr<h5::Group> g = cd(dest);
  return g->remove_group(dir.substr(pos+1));
}

/**
 * Opens an "auto-destructible" HDF5 property list
 */
static void delete_h5plist (hid_t* p) {
  if (*p >= 0) H5Pclose(*p);
  delete p;
  p=0;
}

static boost::shared_ptr<hid_t> open_plist(hid_t classid) {
  boost::shared_ptr<hid_t> retval(new hid_t(-1), std::ptr_fun(delete_h5plist));
  *retval = H5Pcreate(classid);
  if (*retval < 0) {
    throw io::HDF5StatusError("H5Pcreate", *retval);
  }
  return retval;
}

void h5::Group::rename_group(const std::string& from, const std::string& to) {
  boost::shared_ptr<hid_t> create_props = open_plist(H5P_LINK_CREATE);
  H5Pset_create_intermediate_group(*create_props, 1);
  herr_t status = H5Lmove(*m_id, from.c_str(), H5L_SAME_LOC, to.c_str(),
      *create_props, H5P_DEFAULT);
  if (status < 0) throw io::HDF5StatusError("H5Lmove", status);
}

void h5::Group::copy_group(const boost::shared_ptr<h5::Group> other,
    const std::string& dir) {
  std::string::size_type pos = dir.find_last_of('/');
  if (pos == std::string::npos) { //copy on the current group
    const char* use_name = dir.size()?dir.c_str():other->name().c_str();
    herr_t status = H5Ocopy(*other->parent()->location(), 
        other->name().c_str(), *m_id, use_name, H5P_DEFAULT, H5P_DEFAULT);
    if (status < 0) throw io::HDF5StatusError("H5Ocopy", status);

    //read new group contents
    boost::shared_ptr<h5::Group> copied = 
      boost::make_shared<h5::Group>(shared_from_this(), use_name);
    copied->open_recursively();

    //index it
    m_groups[use_name] = copied;

    return;
  }
  
  //if you get to this point, the copy routine needs to be performed on
  //another group, indicated by the path. So, we first cd() there and then do
  //the same as we do here. This will recurse through the directory structure
  //until we find the place defined by the user or return false.
  std::string dest = dir.substr(0, pos);
  if (!dest.size()) dest = "/";
  boost::shared_ptr<h5::Group> g = cd(dest);
  return g->copy_group(other, dir.substr(pos+1));
}

bool h5::Group::has_group(const std::string& dir) const {
  std::string::size_type pos = dir.find_last_of('/');
  if (pos == std::string::npos) { //search on the current group
    typedef std::map<std::string, boost::shared_ptr<h5::Group> > map_type;
    map_type::const_iterator it = m_groups.find(dir);
    return (it != m_groups.end());
  }

  //if you get to this point, the search routine needs to be performed on
  //another group, indicated by the path. So, we first cd() there and then do
  //the same as we do here. This will recurse through the directory structure
  //until we find the place defined by the user or return false.
  std::string dest = dir.substr(0, pos);
  if (!dest.size()) dest = "/";
  boost::shared_ptr<h5::Group> g = cd(dest);
  return g->has_group(dir.substr(pos+1));
}

boost::shared_ptr<h5::Dataset> h5::Group::create_dataset
(const std::string& dir, const bob::io::HDF5Type& type, bool list,
 size_t compression) {
  std::string::size_type pos = dir.find_last_of('/');
  if (pos == std::string::npos) { //creates on the current group
    boost::shared_ptr<h5::Dataset> d = 
      boost::make_shared<h5::Dataset>(shared_from_this(), dir, type,
          list, compression);
    m_datasets[dir] = d;
    return d;
  }

  //if you get to this point, the search routine needs to be performed on
  //another group, indicated by the path. So, we first cd() there and then do
  //the same as we do here. This will recurse through the directory structure
  //until we find the place defined by the user or return false.
  std::string dest = dir.substr(0, pos);
  boost::shared_ptr<h5::Group> g;
  if (!dest.size()) g = cd("/");
  else {
    //let's make sure the directory exists, or let's create it recursively
    if (!has_group(dest)) g = create_group(dest);
    else g = cd(dest);
  }
  return g->create_dataset(dir.substr(pos+1), type, list, compression);
}

void h5::Group::remove_dataset(const std::string& dir) {
  std::string::size_type pos = dir.find_last_of('/');
  if (pos == std::string::npos) { //removes on the current group
    herr_t status = H5Ldelete(*m_id, dir.c_str(), H5P_DEFAULT);
    if (status < 0) throw io::HDF5StatusError("H5Ldelete", status);
    typedef std::map<std::string, boost::shared_ptr<h5::Dataset> > map_type;
    map_type::iterator it = m_datasets.find(dir);
    m_datasets.erase(it);
    return;
  }
  
  //if you get to this point, the removal routine needs to be performed on
  //another group, indicated by the path. So, we first cd() there and then do
  //the same as we do here. This will recurse through the directory structure
  //until we find the place defined by the user or raise an exception.
  std::string dest = dir.substr(0, pos);
  if (!dest.size()) dest = "/";
  boost::shared_ptr<h5::Group> g = cd(dest);
  return g->remove_dataset(dir.substr(pos+1));
}

void h5::Group::rename_dataset(const std::string& from, const std::string& to) {
  boost::shared_ptr<hid_t> create_props = open_plist(H5P_LINK_CREATE);
  H5Pset_create_intermediate_group(*create_props, 1);
  herr_t status = H5Lmove(*m_id, from.c_str(), H5L_SAME_LOC, to.c_str(),
      *create_props, H5P_DEFAULT);
  if (status < 0) throw io::HDF5StatusError("H5Ldelete", status);
}

void h5::Group::copy_dataset(const boost::shared_ptr<h5::Dataset> other,
    const std::string& dir) {

  std::string::size_type pos = dir.find_last_of('/');
  if (pos == std::string::npos) { //search on the current group
    const char* use_name = dir.size()?dir.c_str():other->name().c_str();
    herr_t status = H5Ocopy(*other->parent()->location(),
        other->name().c_str(), *m_id, use_name, H5P_DEFAULT, H5P_DEFAULT);
    if (status < 0) throw io::HDF5StatusError("H5Ocopy", status);
    //read new group contents
    m_datasets[use_name] = boost::make_shared<h5::Dataset>(shared_from_this(), use_name);
    return;
  }

  //if you get to this point, the copy routine needs to be performed on
  //another group, indicated by the path. So, we first cd() there and then do
  //the same as we do here. This will recurse through the directory structure
  //until we find the place defined by the user.
  std::string dest = dir.substr(0, pos);
  if (!dest.size()) dest = "/";
  boost::shared_ptr<h5::Group> g = cd(dest);
  return g->copy_dataset(other, dir.substr(pos+1));
}

bool h5::Group::has_dataset(const std::string& dir) const {
  std::string::size_type pos = dir.find_last_of('/');
  if (pos == std::string::npos) { //search on the current group
    typedef std::map<std::string, boost::shared_ptr<h5::Dataset> > map_type;
    map_type::const_iterator it = m_datasets.find(dir);
    return (it != m_datasets.end());
  }

  //if you get to this point, the search routine needs to be performed on
  //another group, indicated by the path. So, we first cd() there and then do
  //the same as we do here. This will recurse through the directory structure
  //until we find the place defined by the user or return false.
  std::string dest = dir.substr(0, pos);
  if (!dest.size()) dest = "/";
  boost::shared_ptr<h5::Group> g = cd(dest);
  return g->has_dataset(dir.substr(pos+1));
}

bool h5::Group::has_attribute(const std::string& name) const {
  return H5Aexists(*m_id, name.c_str());
}

/**
 * Opens an "auto-destructible" HDF5 dataspace
 */
static void delete_h5dataspace (hid_t* p) {
  if (*p >= 0) H5Sclose(*p);
  delete p;
  p=0;
}

static boost::shared_ptr<hid_t> open_memspace(const io::HDF5Type& t) {
  boost::shared_ptr<hid_t> retval(new hid_t(-1), std::ptr_fun(delete_h5dataspace));
  *retval = H5Screate_simple(t.shape().n(), t.shape().get(), 0);
  if (*retval < 0) throw io::HDF5StatusError("H5Screate_simple", *retval);
  return retval;
}

/**
 * Opens an "auto-destructible" HDF5 attribute
 */
static void delete_h5attribute (hid_t* p) {
  if (*p >= 0) H5Aclose(*p);
  delete p;
  p=0;
}

/**
 * Auto-destructing HDF5 type
 */
static void delete_h5type (hid_t* p) {
  if (*p >= 0) H5Tclose(*p);
  delete p;
  p=0;
}

static boost::shared_ptr<hid_t> open_attribute(boost::shared_ptr<const h5::Group> loc, const std::string& name, const io::HDF5Type& t) {

  boost::shared_ptr<hid_t> retval(new hid_t(-1), 
      std::ptr_fun(delete_h5attribute));

  *retval = H5Aopen(*loc->location(), name.c_str(), H5P_DEFAULT);

  if (*retval < 0) throw io::HDF5StatusError("H5Aopen", *retval);

  //checks if the opened attribute is compatible w/ the expected type
  boost::shared_ptr<hid_t> atype(new hid_t(-1), std::ptr_fun(delete_h5type));
  *atype = H5Aget_type(*retval);
  if (*atype < 0) throw io::HDF5StatusError("H5Aget_type", *atype);

  io::HDF5Type expected(atype);

  if (expected != t) {
    boost::format m("Trying to access attribute '%s' at `%s:%s' with incompatible buffer - expected `%s', but you gave me `%s'");
    m % name % loc->file()->filename() % loc->path() % expected.type_str() % t.type_str();
    throw std::runtime_error(m.str().c_str());
  }

  return retval;
}

static void del_attribute (boost::shared_ptr<hid_t> loc,
    const std::string& name) {
  herr_t err = H5Adelete(*loc, name.c_str());
  if (err < 0) throw io::HDF5StatusError("H5Adelete", err);
}

void h5::Group::delete_attribute (const std::string& name) {
  del_attribute(m_id, name);
}

void h5::Group::read_attribute (const std::string& name,
    const bob::io::HDF5Type& dest, void* buffer) const {
  boost::shared_ptr<hid_t> attribute = open_attribute(shared_from_this(), 
      name, dest);
  herr_t err = H5Aread(*attribute, *dest.htype(), buffer);
  if (err < 0) throw io::HDF5StatusError("H5Aread", err);
}

static boost::shared_ptr<hid_t> create_attribute(boost::shared_ptr<hid_t> loc,
    const std::string& name, const io::HDF5Type& t, 
    boost::shared_ptr<hid_t> space) {

  boost::shared_ptr<hid_t> retval(new hid_t(-1), 
      std::ptr_fun(delete_h5attribute));

  *retval = H5Acreate(*loc, name.c_str(), *t.htype(), *space, H5P_DEFAULT,
      H5P_DEFAULT);

  if (*retval < 0) throw io::HDF5StatusError("H5Acreate", *retval);
  return retval;
}

void h5::Group::write_attribute (const std::string& name,
    const bob::io::HDF5Type& dest,
    const void* buffer) {

  boost::shared_ptr<hid_t> dataspace = open_memspace(dest);

  if (has_attribute(name)) delete_attribute(name);
  boost::shared_ptr<hid_t> attribute =
    create_attribute(m_id, name, dest, dataspace);
  
  /* Write the attribute data. */
  herr_t err = H5Awrite(*attribute, *dest.htype(), buffer);
  if (err < 0) throw io::HDF5StatusError("H5Awrite", err);
}

h5::RootGroup::RootGroup(boost::shared_ptr<h5::File> parent):
  h5::Group(parent),
  m_parent(parent)
{
}

h5::RootGroup::~RootGroup() {
}

const std::string& h5::RootGroup::filename() const {
  return parent()->filename();
}
