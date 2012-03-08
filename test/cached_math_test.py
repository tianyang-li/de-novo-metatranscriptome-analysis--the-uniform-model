#!/usr/bin/env python

import unittest
import random
from test import test_support
from nzmath.combinatorial import stirling2
from scipy.misc import comb, factorial

import metatranscriptome_uniform_de_novo._cached_math as cm

class TestFact(unittest.TestCase):
    def test_fact(self):
        for i in xrange(1000):
            n = random.randint(0, 10000)
            self.assertEqual(cm.fact(n), factorial(n, exact=1), "fix factorial")

class TestComb(unittest.TestCase):    
    def test_comb(self):
        for i in xrange(1000):
            n = random.randint(0, 5000)
            k = random.randint(0, n)
            a = cm.binom(n, k)
            b = comb(n, k, exact=1)
            self.assertEqual(a, b, "n %d k %d mine %d correct %d" % (n, k, a, b))
        
def test_main():
    test_support.run_unittest()

if __name__ == '__main__':
    test_main()



