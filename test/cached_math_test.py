#!/usr/bin/env python

import unittest
import random
from test import test_support
from nzmath.combinatorial import stirling2
from scipy.misc import comb, factorial

import metatranscriptome_uniform_de_novo._cached_math as cm

class TestFact(unittest.TestCase):
    def test_fact(self):
        for i in xrange(10000):
            n = random.randint(0, 10000)
            self.assertEqual(cm.fact(n) , factorial(n, exact=1), "fix factorial")
        
def test_main():
    test_support.run_unittest(TestFact)

if __name__ == '__main__':
    test_main()



