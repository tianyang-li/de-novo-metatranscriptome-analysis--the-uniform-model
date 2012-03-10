#!/usr/bin/env python

import random
import unittest
from test import test_support
from nzmath.combinatorial import stirling2
from scipy.misc import comb, factorial

import metatranscriptome_uniform_de_novo._cached_math as cm
import metatranscriptome_uniform_de_novo._math as rm

class TestFactStl2(unittest.TestCase):
    def test_fact_stl2(self):
        for i in xrange(100):
            n = random.randint(0, 1000)
            k = random.randint(0, n)
            a = cm.fact(k) * stirling2(n, k)
            b = cm.fact_stl2(n, k)
            self.assertEqual(a, b, "fix simple version")
            
            
            
def test_main():
    test_support.run_unittest(TestFactStl2)

if __name__=='__main__':
    test_main()


