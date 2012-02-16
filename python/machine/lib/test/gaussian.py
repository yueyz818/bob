#!/usr/bin/env python
# vim: set fileencoding=utf-8 :
# Laurent El Shafey <Laurent.El-Shafey@idiap.ch>
# Thu Feb 16 16:54:45 2012 +0200
#
# Copyright (C) 2011-2012 Idiap Research Institute, Martigny, Switzerland
# 
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, version 3 of the License.
# 
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
# 
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.

"""Tests the Gaussian machine
"""

import os, sys
import unittest
import bob
import numpy
import tempfile


class GaussianMachineTest(unittest.TestCase):
  """Performs various Gaussian machine tests."""

  def test01_GaussianMachine(self):
    """Test a GaussianMachine"""

    # Initializes a Gaussian with zero mean and unit variance
    g = bob.machine.Gaussian(3)
    self.assertTrue( (g.mean == 0.0).all() )
    self.assertTrue( (g.variance == 1.0).all() )
    self.assertTrue( g.DimD == 3 )

    # Set and check mean, variance, variance thresholds 
    mean     = numpy.array([0, 1, 2], 'float64')
    variance = numpy.array([3, 2, 1], 'float64')
    g.mean     = mean
    g.variance = variance
    g.setVarianceThresholds(0.0005)
    self.assertTrue( (g.mean == mean).all() )
    self.assertTrue( (g.variance == variance).all() )
    self.assertTrue( (g.varianceThresholds == 0.0005).all() )
    
    # Save and read from file
    filename = str(tempfile.mkstemp(".hdf5")[1])
    g.save(bob.io.HDF5File(filename))
    g_loaded = bob.machine.Gaussian(bob.io.HDF5File(filename))
    self.assertTrue( g == g_loaded )
    # Make them different
    g_loaded.setVarianceThresholds(0.001)
    self.assertFalse( g == g_loaded )

    # Check likelihood computation
    sample1 = numpy.array([0, 1, 2], 'float64')
    sample2 = numpy.array([1, 2, 3], 'float64')
    sample3 = numpy.array([2, 3, 4], 'float64')
    ref1 = -3.652695334228046
    ref2 = -4.569362000894712
    ref3 = -7.319362000894712
    eps = 1e-10
    self.assertTrue( abs(g.logLikelihood(sample1) - ref1) < eps)
    self.assertTrue( abs(g.forward(sample1) - ref1) < eps)
    self.assertTrue( abs(g.logLikelihood(sample2) - ref2) < eps)
    self.assertTrue( abs(g.forward(sample2) - ref2) < eps)
    self.assertTrue( abs(g.logLikelihood(sample3) - ref3) < eps)
    self.assertTrue( abs(g.forward(sample3) - ref3) < eps)

    # Check resize and assignment
    g.resize(5)
    self.assertTrue( g.DimD == 5 )
    g2 = bob.machine.Gaussian()
    g2 = g
    self.assertTrue( g == g2 )

# Instantiates our standard main module for unittests
main = bob.helper.unittest_main(GaussianMachineTest)
