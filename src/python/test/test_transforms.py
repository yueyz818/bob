#!/usr/bin/env python
# vim: set fileencoding=utf-8 :
# Andre Anjos <andre.anjos@idiap.ch>
# Wed 25 Aug 2010 12:33:13 CEST 

import os, sys
import unittest
import torch

def compare(v1, v2, width):
  return abs(v1-v2) <= width

class TransformTest(unittest.TestCase):
  """Performs for dct, dct2, fft, fft2 and their inverses"""
  
  def test_dct_1(self):

    # set up simple tensor (have to be 2d)
    t = torch.core.FloatTensor(2, 2)
    t.set(0, 0, 1.0)
    t.set(0, 1, 0.0)
    t.set(1, 0, 0.0)
    t.set(1, 1, 0.0)

    # process using DCT
    d = torch.sp.spDCT()
    d.process(t)
    self.assertEqual(d.getNOutputs(), 1)

    # get answer and compare to matlabs dct2 (warning do not use dct)
    tt = d.getOutput(0)

    self.assertTrue(compare(tt.get(0,0), 0.5, 1e-2))
    self.assertTrue(compare(tt.get(0,1), 0.5, 1e-2))
    self.assertTrue(compare(tt.get(1,0), 0.5, 1e-2))
    self.assertTrue(compare(tt.get(1,1), 0.5, 1e-2))
    
  def test_dct_2(self):

    # set up simple tensor (have to be 2d)
    t = torch.core.FloatTensor(4, 4)

    for i in range(4):
      for j in range(4):
        t.set(i, j, 1.0+i+j)

    # process using DCT
    d = torch.sp.spDCT()
    d.process(t)
    self.assertEqual(d.getNOutputs(), 1)

    # get answer and compare to matlabs dct2 (warning do not use dct)
    tt = d.getOutput(0)

    self.assertTrue(compare(tt.get(0,0), 16.0000, 1e-3))
    self.assertTrue(compare(tt.get(0,1), -4.4609, 1e-3))
    self.assertTrue(compare(tt.get(0,2),  0.0000, 1e-3))
    self.assertTrue(compare(tt.get(0,3), -0.3170, 1e-3))

    self.assertTrue(compare(tt.get(1,0), -4.4609, 1e-3))
    self.assertTrue(compare(tt.get(1,1),  0.0000, 1e-3))
    self.assertTrue(compare(tt.get(1,2),  0.0000, 1e-3))
    self.assertTrue(compare(tt.get(1,3),  0.0000, 1e-3))

    self.assertTrue(compare(tt.get(2,0), 0.0000, 1e-3))
    self.assertTrue(compare(tt.get(2,1), 0.0000, 1e-3))
    self.assertTrue(compare(tt.get(2,2), 0.0000, 1e-3))
    self.assertTrue(compare(tt.get(2,3), 0.0000, 1e-3))

    self.assertTrue(compare(tt.get(3,0), -0.3170, 1e-3))
    self.assertTrue(compare(tt.get(3,1),  0.0000, 1e-3))
    self.assertTrue(compare(tt.get(3,2),  0.0000, 1e-3))
    self.assertTrue(compare(tt.get(3,3),  0.0000, 1e-3))

  def test_dct_8(self):

    # set up simple tensor (have to be 2d)
    t = torch.core.FloatTensor(8, 8)

    for i in range(8):
      for j in range(8):
        t.set(i, j, 1.0+i+j)

    # process using DCT
    d = torch.sp.spDCT()
    d.process(t)
    self.assertEqual(d.getNOutputs(), 1)

    # get answer and compare to matlabs dct2 (warning do not use dct)
    tt = d.getOutput(0)

    self.assertTrue(compare(tt.get(0,0), 64.00000, 1e-3))
    self.assertTrue(compare(tt.get(0,1), -18.2216, 1e-3))
    self.assertTrue(compare(tt.get(0,2),   0.0000, 1e-3))
    self.assertTrue(compare(tt.get(0,3),  -1.9048, 1e-3))
    self.assertTrue(compare(tt.get(0,4),   0.0000, 1e-3))
    self.assertTrue(compare(tt.get(0,5),  -0.5682, 1e-3))
    self.assertTrue(compare(tt.get(0,6),   0.0000, 1e-3))
    self.assertTrue(compare(tt.get(0,7),  -0.1434, 1e-3))

    self.assertTrue(compare(tt.get(1,0), -18.2216, 1e-3))
    self.assertTrue(compare(tt.get(1,1),   0.0000, 1e-3))
    self.assertTrue(compare(tt.get(1,2),   0.0000, 1e-3))
    self.assertTrue(compare(tt.get(1,3),   0.0000, 1e-3))
    self.assertTrue(compare(tt.get(1,4),   0.0000, 1e-3))
    self.assertTrue(compare(tt.get(1,5),   0.0000, 1e-3))
    self.assertTrue(compare(tt.get(1,6),   0.0000, 1e-3))
    self.assertTrue(compare(tt.get(1,7),   0.0000, 1e-3))

    self.assertTrue(compare(tt.get(2,0), 0.0000, 1e-3))
    self.assertTrue(compare(tt.get(2,1), 0.0000, 1e-3))
    self.assertTrue(compare(tt.get(2,2), 0.0000, 1e-3))
    self.assertTrue(compare(tt.get(2,3), 0.0000, 1e-3))
    self.assertTrue(compare(tt.get(2,4), 0.0000, 1e-3))
    self.assertTrue(compare(tt.get(2,5), 0.0000, 1e-3))
    self.assertTrue(compare(tt.get(2,6), 0.0000, 1e-3))
    self.assertTrue(compare(tt.get(2,7), 0.0000, 1e-3))

    self.assertTrue(compare(tt.get(3,0), -1.9048, 1e-3))
    self.assertTrue(compare(tt.get(3,1),  0.0000, 1e-3))
    self.assertTrue(compare(tt.get(3,2),  0.0000, 1e-3))
    self.assertTrue(compare(tt.get(3,3),  0.0000, 1e-3))
    self.assertTrue(compare(tt.get(3,4),  0.0000, 1e-3))
    self.assertTrue(compare(tt.get(3,5),  0.0000, 1e-3))
    self.assertTrue(compare(tt.get(3,6),  0.0000, 1e-3))
    self.assertTrue(compare(tt.get(3,7),  0.0000, 1e-3))

    self.assertTrue(compare(tt.get(4,0), 0.0000, 1e-3))
    self.assertTrue(compare(tt.get(4,1), 0.0000, 1e-3))
    self.assertTrue(compare(tt.get(4,2), 0.0000, 1e-3))
    self.assertTrue(compare(tt.get(4,3), 0.0000, 1e-3))
    self.assertTrue(compare(tt.get(4,4), 0.0000, 1e-3))
    self.assertTrue(compare(tt.get(4,5), 0.0000, 1e-3))
    self.assertTrue(compare(tt.get(4,6), 0.0000, 1e-3))
    self.assertTrue(compare(tt.get(4,7), 0.0000, 1e-3))

    self.assertTrue(compare(tt.get(5,0), -0.5682, 1e-3))
    self.assertTrue(compare(tt.get(5,1),  0.0000, 1e-3))
    self.assertTrue(compare(tt.get(5,2),  0.0000, 1e-3))
    self.assertTrue(compare(tt.get(5,3),  0.0000, 1e-3))
    self.assertTrue(compare(tt.get(5,4),  0.0000, 1e-3))
    self.assertTrue(compare(tt.get(5,5),  0.0000, 1e-3))
    self.assertTrue(compare(tt.get(5,6),  0.0000, 1e-3))
    self.assertTrue(compare(tt.get(5,7),  0.0000, 1e-3))

    self.assertTrue(compare(tt.get(6,0), 0.0000, 1e-3))
    self.assertTrue(compare(tt.get(6,1), 0.0000, 1e-3))
    self.assertTrue(compare(tt.get(6,2), 0.0000, 1e-3))
    self.assertTrue(compare(tt.get(6,3), 0.0000, 1e-3))
    self.assertTrue(compare(tt.get(6,4), 0.0000, 1e-3))
    self.assertTrue(compare(tt.get(6,5), 0.0000, 1e-3))
    self.assertTrue(compare(tt.get(6,6), 0.0000, 1e-3))
    self.assertTrue(compare(tt.get(6,7), 0.0000, 1e-3))

    self.assertTrue(compare(tt.get(7,0), -0.1434, 1e-3))
    self.assertTrue(compare(tt.get(7,1),  0.0000, 1e-3))
    self.assertTrue(compare(tt.get(7,2),  0.0000, 1e-3))
    self.assertTrue(compare(tt.get(7,3),  0.0000, 1e-3))
    self.assertTrue(compare(tt.get(7,4),  0.0000, 1e-3))
    self.assertTrue(compare(tt.get(7,5),  0.0000, 1e-3))
    self.assertTrue(compare(tt.get(7,6),  0.0000, 1e-3))
    self.assertTrue(compare(tt.get(7,7),  0.0000, 1e-3))

  def test_dct_16(self):

    # set up simple tensor (have to be 2d)
    t = torch.core.FloatTensor(16, 16)

    for i in range(16):
      for j in range(16):
        t.set(i, j, 1.0+i+j)

    # process using DCT
    d = torch.sp.spDCT()
    d.process(t)
    self.assertEqual(d.getNOutputs(), 1)

    # get answer and compare to matlabs dct2 (warning do not use dct)
    tt = d.getOutput(0)

    self.assertTrue(compare(tt.get(0, 0), 256.0000, 1e-3))
    self.assertTrue(compare(tt.get(0, 1), -73.2461, 1e-3))
    self.assertTrue(compare(tt.get(0, 2),   0.0000, 1e-3))
    self.assertTrue(compare(tt.get(0, 3),  -8.0301, 1e-3))
    self.assertTrue(compare(tt.get(0, 4),   0.0000, 1e-3))
    self.assertTrue(compare(tt.get(0, 5),  -2.8063, 1e-3))
    self.assertTrue(compare(tt.get(0, 6),   0.0000, 1e-3))
    self.assertTrue(compare(tt.get(0, 7),  -1.3582, 1e-3))
    self.assertTrue(compare(tt.get(0, 8),   0.0000, 1e-3))
    self.assertTrue(compare(tt.get(0, 9),  -0.7507, 1e-3))
    self.assertTrue(compare(tt.get(0,10),   0.0000, 1e-3))
    self.assertTrue(compare(tt.get(0,11),  -0.4286, 1e-3))
    self.assertTrue(compare(tt.get(0,12),   0.0000, 1e-3))
    self.assertTrue(compare(tt.get(0,13),  -0.2242, 1e-3))
    self.assertTrue(compare(tt.get(0,14),   0.0000, 1e-3))
    self.assertTrue(compare(tt.get(0,15),  -0.0700, 1e-3))

    self.assertTrue(compare(tt.get(1, 0), -73.2461, 1e-3))
    self.assertTrue(compare(tt.get(1, 1),   0.0000, 1e-3))
    self.assertTrue(compare(tt.get(1, 2),   0.0000, 1e-3))
    self.assertTrue(compare(tt.get(1, 3),   0.0000, 1e-3))
    self.assertTrue(compare(tt.get(1, 4),   0.0000, 1e-3))
    self.assertTrue(compare(tt.get(1, 5),   0.0000, 1e-3))
    self.assertTrue(compare(tt.get(1, 6),   0.0000, 1e-3))
    self.assertTrue(compare(tt.get(1, 7),   0.0000, 1e-3))
    self.assertTrue(compare(tt.get(1, 8),   0.0000, 1e-3))
    self.assertTrue(compare(tt.get(1, 9),   0.0000, 1e-3))
    self.assertTrue(compare(tt.get(1,10),   0.0000, 1e-3))
    self.assertTrue(compare(tt.get(1,11),   0.0000, 1e-3))
    self.assertTrue(compare(tt.get(1,12),   0.0000, 1e-3))
    self.assertTrue(compare(tt.get(1,13),   0.0000, 1e-3))
    self.assertTrue(compare(tt.get(1,14),   0.0000, 1e-3))
    self.assertTrue(compare(tt.get(1,15),   0.0000, 1e-3))

    self.assertTrue(compare(tt.get(2, 0),   0.0000, 1e-3))
    self.assertTrue(compare(tt.get(2, 1),   0.0000, 1e-3))
    self.assertTrue(compare(tt.get(2, 2),   0.0000, 1e-3))
    self.assertTrue(compare(tt.get(2, 3),   0.0000, 1e-3))
    self.assertTrue(compare(tt.get(2, 4),   0.0000, 1e-3))
    self.assertTrue(compare(tt.get(2, 5),   0.0000, 1e-3))
    self.assertTrue(compare(tt.get(2, 6),   0.0000, 1e-3))
    self.assertTrue(compare(tt.get(2, 7),   0.0000, 1e-3))
    self.assertTrue(compare(tt.get(2, 8),   0.0000, 1e-3))
    self.assertTrue(compare(tt.get(2, 9),   0.0000, 1e-3))
    self.assertTrue(compare(tt.get(2,10),   0.0000, 1e-3))
    self.assertTrue(compare(tt.get(2,11),   0.0000, 1e-3))
    self.assertTrue(compare(tt.get(2,12),   0.0000, 1e-3))
    self.assertTrue(compare(tt.get(2,13),   0.0000, 1e-3))
    self.assertTrue(compare(tt.get(2,14),   0.0000, 1e-3))
    self.assertTrue(compare(tt.get(2,15),   0.0000, 1e-3))

    self.assertTrue(compare(tt.get(3, 0), -8.0301, 1e-3))
    self.assertTrue(compare(tt.get(3, 1),  0.0000, 1e-3))
    self.assertTrue(compare(tt.get(3, 2),  0.0000, 1e-3))
    self.assertTrue(compare(tt.get(3, 3),  0.0000, 1e-3))
    self.assertTrue(compare(tt.get(3, 4),  0.0000, 1e-3))
    self.assertTrue(compare(tt.get(3, 5),  0.0000, 1e-3))
    self.assertTrue(compare(tt.get(3, 6),  0.0000, 1e-3))
    self.assertTrue(compare(tt.get(3, 7),  0.0000, 1e-3))
    self.assertTrue(compare(tt.get(3, 8),  0.0000, 1e-3))
    self.assertTrue(compare(tt.get(3, 9),  0.0000, 1e-3))
    self.assertTrue(compare(tt.get(3,10),  0.0000, 1e-3))
    self.assertTrue(compare(tt.get(3,11),  0.0000, 1e-3))
    self.assertTrue(compare(tt.get(3,12),  0.0000, 1e-3))
    self.assertTrue(compare(tt.get(3,13),  0.0000, 1e-3))
    self.assertTrue(compare(tt.get(3,14),  0.0000, 1e-3))
    self.assertTrue(compare(tt.get(3,15),  0.0000, 1e-3))

    self.assertTrue(compare(tt.get(4, 0),   0.0000, 1e-3))
    self.assertTrue(compare(tt.get(4, 1),   0.0000, 1e-3))
    self.assertTrue(compare(tt.get(4, 2),   0.0000, 1e-3))
    self.assertTrue(compare(tt.get(4, 3),   0.0000, 1e-3))
    self.assertTrue(compare(tt.get(4, 4),   0.0000, 1e-3))
    self.assertTrue(compare(tt.get(4, 5),   0.0000, 1e-3))
    self.assertTrue(compare(tt.get(4, 6),   0.0000, 1e-3))
    self.assertTrue(compare(tt.get(4, 7),   0.0000, 1e-3))
    self.assertTrue(compare(tt.get(4, 8),   0.0000, 1e-3))
    self.assertTrue(compare(tt.get(4, 9),   0.0000, 1e-3))
    self.assertTrue(compare(tt.get(4,10),   0.0000, 1e-3))
    self.assertTrue(compare(tt.get(4,11),   0.0000, 1e-3))
    self.assertTrue(compare(tt.get(4,12),   0.0000, 1e-3))
    self.assertTrue(compare(tt.get(4,13),   0.0000, 1e-3))
    self.assertTrue(compare(tt.get(4,14),   0.0000, 1e-3))
    self.assertTrue(compare(tt.get(4,15),   0.0000, 1e-3))

    self.assertTrue(compare(tt.get(5, 0), -2.8063, 1e-3))
    self.assertTrue(compare(tt.get(5, 1),  0.0000, 1e-3))
    self.assertTrue(compare(tt.get(5, 2),  0.0000, 1e-3))
    self.assertTrue(compare(tt.get(5, 3),  0.0000, 1e-3))
    self.assertTrue(compare(tt.get(5, 4),  0.0000, 1e-3))
    self.assertTrue(compare(tt.get(5, 5),  0.0000, 1e-3))
    self.assertTrue(compare(tt.get(5, 6),  0.0000, 1e-3))
    self.assertTrue(compare(tt.get(5, 7),  0.0000, 1e-3))
    self.assertTrue(compare(tt.get(5, 8),  0.0000, 1e-3))
    self.assertTrue(compare(tt.get(5, 9),  0.0000, 1e-3))
    self.assertTrue(compare(tt.get(5,10),  0.0000, 1e-3))
    self.assertTrue(compare(tt.get(5,11),  0.0000, 1e-3))
    self.assertTrue(compare(tt.get(5,12),  0.0000, 1e-3))
    self.assertTrue(compare(tt.get(5,13),  0.0000, 1e-3))
    self.assertTrue(compare(tt.get(5,14),  0.0000, 1e-3))
    self.assertTrue(compare(tt.get(5,15),  0.0000, 1e-3))

    self.assertTrue(compare(tt.get(6, 0),   0.0000, 1e-3))
    self.assertTrue(compare(tt.get(6, 1),   0.0000, 1e-3))
    self.assertTrue(compare(tt.get(6, 2),   0.0000, 1e-3))
    self.assertTrue(compare(tt.get(6, 3),   0.0000, 1e-3))
    self.assertTrue(compare(tt.get(6, 4),   0.0000, 1e-3))
    self.assertTrue(compare(tt.get(6, 5),   0.0000, 1e-3))
    self.assertTrue(compare(tt.get(6, 6),   0.0000, 1e-3))
    self.assertTrue(compare(tt.get(6, 7),   0.0000, 1e-3))
    self.assertTrue(compare(tt.get(6, 8),   0.0000, 1e-3))
    self.assertTrue(compare(tt.get(6, 9),   0.0000, 1e-3))
    self.assertTrue(compare(tt.get(6,10),   0.0000, 1e-3))
    self.assertTrue(compare(tt.get(6,11),   0.0000, 1e-3))
    self.assertTrue(compare(tt.get(6,12),   0.0000, 1e-3))
    self.assertTrue(compare(tt.get(6,13),   0.0000, 1e-3))
    self.assertTrue(compare(tt.get(6,14),   0.0000, 1e-3))
    self.assertTrue(compare(tt.get(6,15),   0.0000, 1e-3))

    self.assertTrue(compare(tt.get(7, 0), -1.3582, 1e-3))
    self.assertTrue(compare(tt.get(7, 1),  0.0000, 1e-3))
    self.assertTrue(compare(tt.get(7, 2),  0.0000, 1e-3))
    self.assertTrue(compare(tt.get(7, 3),  0.0000, 1e-3))
    self.assertTrue(compare(tt.get(7, 4),  0.0000, 1e-3))
    self.assertTrue(compare(tt.get(7, 5),  0.0000, 1e-3))
    self.assertTrue(compare(tt.get(7, 6),  0.0000, 1e-3))
    self.assertTrue(compare(tt.get(7, 7),  0.0000, 1e-3))
    self.assertTrue(compare(tt.get(7, 8),  0.0000, 1e-3))
    self.assertTrue(compare(tt.get(7, 9),  0.0000, 1e-3))
    self.assertTrue(compare(tt.get(7,10),  0.0000, 1e-3))
    self.assertTrue(compare(tt.get(7,11),  0.0000, 1e-3))
    self.assertTrue(compare(tt.get(7,12),  0.0000, 1e-3))
    self.assertTrue(compare(tt.get(7,13),  0.0000, 1e-3))
    self.assertTrue(compare(tt.get(7,14),  0.0000, 1e-3))
    self.assertTrue(compare(tt.get(7,15),  0.0000, 1e-3))

    self.assertTrue(compare(tt.get(8, 0),   0.0000, 1e-3))
    self.assertTrue(compare(tt.get(8, 1),   0.0000, 1e-3))
    self.assertTrue(compare(tt.get(8, 2),   0.0000, 1e-3))
    self.assertTrue(compare(tt.get(8, 3),   0.0000, 1e-3))
    self.assertTrue(compare(tt.get(8, 4),   0.0000, 1e-3))
    self.assertTrue(compare(tt.get(8, 5),   0.0000, 1e-3))
    self.assertTrue(compare(tt.get(8, 6),   0.0000, 1e-3))
    self.assertTrue(compare(tt.get(8, 7),   0.0000, 1e-3))
    self.assertTrue(compare(tt.get(8, 8),   0.0000, 1e-3))
    self.assertTrue(compare(tt.get(8, 9),   0.0000, 1e-3))
    self.assertTrue(compare(tt.get(8,10),   0.0000, 1e-3))
    self.assertTrue(compare(tt.get(8,11),   0.0000, 1e-3))
    self.assertTrue(compare(tt.get(8,12),   0.0000, 1e-3))
    self.assertTrue(compare(tt.get(8,13),   0.0000, 1e-3))
    self.assertTrue(compare(tt.get(8,14),   0.0000, 1e-3))
    self.assertTrue(compare(tt.get(8,15),   0.0000, 1e-3))

    self.assertTrue(compare(tt.get(9, 0), -0.7507, 1e-3))
    self.assertTrue(compare(tt.get(9, 1),  0.0000, 1e-3))
    self.assertTrue(compare(tt.get(9, 2),  0.0000, 1e-3))
    self.assertTrue(compare(tt.get(9, 3),  0.0000, 1e-3))
    self.assertTrue(compare(tt.get(9, 4),  0.0000, 1e-3))
    self.assertTrue(compare(tt.get(9, 5),  0.0000, 1e-3))
    self.assertTrue(compare(tt.get(9, 6),  0.0000, 1e-3))
    self.assertTrue(compare(tt.get(9, 7),  0.0000, 1e-3))
    self.assertTrue(compare(tt.get(9, 8),  0.0000, 1e-3))
    self.assertTrue(compare(tt.get(9, 9),  0.0000, 1e-3))
    self.assertTrue(compare(tt.get(9,10),  0.0000, 1e-3))
    self.assertTrue(compare(tt.get(9,11),  0.0000, 1e-3))
    self.assertTrue(compare(tt.get(9,12),  0.0000, 1e-3))
    self.assertTrue(compare(tt.get(9,13),  0.0000, 1e-3))
    self.assertTrue(compare(tt.get(9,14),  0.0000, 1e-3))
    self.assertTrue(compare(tt.get(9,15),  0.0000, 1e-3))

    self.assertTrue(compare(tt.get(10, 0),   0.0000, 1e-3))
    self.assertTrue(compare(tt.get(10, 1),   0.0000, 1e-3))
    self.assertTrue(compare(tt.get(10, 2),   0.0000, 1e-3))
    self.assertTrue(compare(tt.get(10, 3),   0.0000, 1e-3))
    self.assertTrue(compare(tt.get(10, 4),   0.0000, 1e-3))
    self.assertTrue(compare(tt.get(10, 5),   0.0000, 1e-3))
    self.assertTrue(compare(tt.get(10, 6),   0.0000, 1e-3))
    self.assertTrue(compare(tt.get(10, 7),   0.0000, 1e-3))
    self.assertTrue(compare(tt.get(10, 8),   0.0000, 1e-3))
    self.assertTrue(compare(tt.get(10, 9),   0.0000, 1e-3))
    self.assertTrue(compare(tt.get(10,10),   0.0000, 1e-3))
    self.assertTrue(compare(tt.get(10,11),   0.0000, 1e-3))
    self.assertTrue(compare(tt.get(10,12),   0.0000, 1e-3))
    self.assertTrue(compare(tt.get(10,13),   0.0000, 1e-3))
    self.assertTrue(compare(tt.get(10,14),   0.0000, 1e-3))
    self.assertTrue(compare(tt.get(10,15),   0.0000, 1e-3))

    self.assertTrue(compare(tt.get(11, 0), -0.4286, 1e-3))
    self.assertTrue(compare(tt.get(11, 1),  0.0000, 1e-3))
    self.assertTrue(compare(tt.get(11, 2),  0.0000, 1e-3))
    self.assertTrue(compare(tt.get(11, 3),  0.0000, 1e-3))
    self.assertTrue(compare(tt.get(11, 4),  0.0000, 1e-3))
    self.assertTrue(compare(tt.get(11, 5),  0.0000, 1e-3))
    self.assertTrue(compare(tt.get(11, 6),  0.0000, 1e-3))
    self.assertTrue(compare(tt.get(11, 7),  0.0000, 1e-3))
    self.assertTrue(compare(tt.get(11, 8),  0.0000, 1e-3))
    self.assertTrue(compare(tt.get(11, 9),  0.0000, 1e-3))
    self.assertTrue(compare(tt.get(11,10),  0.0000, 1e-3))
    self.assertTrue(compare(tt.get(11,11),  0.0000, 1e-3))
    self.assertTrue(compare(tt.get(11,12),  0.0000, 1e-3))
    self.assertTrue(compare(tt.get(11,13),  0.0000, 1e-3))
    self.assertTrue(compare(tt.get(11,14),  0.0000, 1e-3))
    self.assertTrue(compare(tt.get(11,15),  0.0000, 1e-3))

    self.assertTrue(compare(tt.get(12, 0),   0.0000, 1e-3))
    self.assertTrue(compare(tt.get(12, 1),   0.0000, 1e-3))
    self.assertTrue(compare(tt.get(12, 2),   0.0000, 1e-3))
    self.assertTrue(compare(tt.get(12, 3),   0.0000, 1e-3))
    self.assertTrue(compare(tt.get(12, 4),   0.0000, 1e-3))
    self.assertTrue(compare(tt.get(12, 5),   0.0000, 1e-3))
    self.assertTrue(compare(tt.get(12, 6),   0.0000, 1e-3))
    self.assertTrue(compare(tt.get(12, 7),   0.0000, 1e-3))
    self.assertTrue(compare(tt.get(12, 8),   0.0000, 1e-3))
    self.assertTrue(compare(tt.get(12, 9),   0.0000, 1e-3))
    self.assertTrue(compare(tt.get(12,10),   0.0000, 1e-3))
    self.assertTrue(compare(tt.get(12,11),   0.0000, 1e-3))
    self.assertTrue(compare(tt.get(12,12),   0.0000, 1e-3))
    self.assertTrue(compare(tt.get(12,13),   0.0000, 1e-3))
    self.assertTrue(compare(tt.get(12,14),   0.0000, 1e-3))
    self.assertTrue(compare(tt.get(12,15),   0.0000, 1e-3))

    self.assertTrue(compare(tt.get(13, 0), -0.2242, 1e-3))
    self.assertTrue(compare(tt.get(13, 1),  0.0000, 1e-3))
    self.assertTrue(compare(tt.get(13, 2),  0.0000, 1e-3))
    self.assertTrue(compare(tt.get(13, 3),  0.0000, 1e-3))
    self.assertTrue(compare(tt.get(13, 4),  0.0000, 1e-3))
    self.assertTrue(compare(tt.get(13, 5),  0.0000, 1e-3))
    self.assertTrue(compare(tt.get(13, 6),  0.0000, 1e-3))
    self.assertTrue(compare(tt.get(13, 7),  0.0000, 1e-3))
    self.assertTrue(compare(tt.get(13, 8),  0.0000, 1e-3))
    self.assertTrue(compare(tt.get(13, 9),  0.0000, 1e-3))
    self.assertTrue(compare(tt.get(13,10),  0.0000, 1e-3))
    self.assertTrue(compare(tt.get(13,11),  0.0000, 1e-3))
    self.assertTrue(compare(tt.get(13,12),  0.0000, 1e-3))
    self.assertTrue(compare(tt.get(13,13),  0.0000, 1e-3))
    self.assertTrue(compare(tt.get(13,14),  0.0000, 1e-3))
    self.assertTrue(compare(tt.get(13,15),  0.0000, 1e-3))

    self.assertTrue(compare(tt.get(14, 0),   0.0000, 1e-3))
    self.assertTrue(compare(tt.get(14, 1),   0.0000, 1e-3))
    self.assertTrue(compare(tt.get(14, 2),   0.0000, 1e-3))
    self.assertTrue(compare(tt.get(14, 3),   0.0000, 1e-3))
    self.assertTrue(compare(tt.get(14, 4),   0.0000, 1e-3))
    self.assertTrue(compare(tt.get(14, 5),   0.0000, 1e-3))
    self.assertTrue(compare(tt.get(14, 6),   0.0000, 1e-3))
    self.assertTrue(compare(tt.get(14, 7),   0.0000, 1e-3))
    self.assertTrue(compare(tt.get(14, 8),   0.0000, 1e-3))
    self.assertTrue(compare(tt.get(14, 9),   0.0000, 1e-3))
    self.assertTrue(compare(tt.get(14,10),   0.0000, 1e-3))
    self.assertTrue(compare(tt.get(14,11),   0.0000, 1e-3))
    self.assertTrue(compare(tt.get(14,12),   0.0000, 1e-3))
    self.assertTrue(compare(tt.get(14,13),   0.0000, 1e-3))
    self.assertTrue(compare(tt.get(14,14),   0.0000, 1e-3))
    self.assertTrue(compare(tt.get(14,15),   0.0000, 1e-3))

    self.assertTrue(compare(tt.get(15, 0), -0.0700, 1e-3))
    self.assertTrue(compare(tt.get(15, 1),  0.0000, 1e-3))
    self.assertTrue(compare(tt.get(15, 2),  0.0000, 1e-3))
    self.assertTrue(compare(tt.get(15, 3),  0.0000, 1e-3))
    self.assertTrue(compare(tt.get(15, 4),  0.0000, 1e-3))
    self.assertTrue(compare(tt.get(15, 5),  0.0000, 1e-3))
    self.assertTrue(compare(tt.get(15, 6),  0.0000, 1e-3))
    self.assertTrue(compare(tt.get(15, 7),  0.0000, 1e-3))
    self.assertTrue(compare(tt.get(15, 8),  0.0000, 1e-3))
    self.assertTrue(compare(tt.get(15, 9),  0.0000, 1e-3))
    self.assertTrue(compare(tt.get(15,10),  0.0000, 1e-3))
    self.assertTrue(compare(tt.get(15,11),  0.0000, 1e-3))
    self.assertTrue(compare(tt.get(15,12),  0.0000, 1e-3))
    self.assertTrue(compare(tt.get(15,13),  0.0000, 1e-3))
    self.assertTrue(compare(tt.get(15,14),  0.0000, 1e-3))
    self.assertTrue(compare(tt.get(15,15),  0.0000, 1e-3))

if __name__ == '__main__':
  sys.argv.append('-v')
  if os.environ.has_key('TORCH_PROFILE') and \
      os.environ['TORCH_PROFILE'] and \
      hasattr(torch.core, 'ProfilerStart'):
    torch.core.ProfilerStart(os.environ['TORCH_PROFILE'])
  os.chdir(os.path.realpath(os.path.dirname(sys.argv[0])))
  unittest.main()
  if os.environ.has_key('TORCH_PROFILE') and \
      os.environ['TORCH_PROFILE'] and \
      hasattr(torch.core, 'ProfilerStop'):
    torch.core.ProfilerStop()
