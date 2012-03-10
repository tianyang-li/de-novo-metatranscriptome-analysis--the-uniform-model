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
            n = random.randint(0, 2000)
            self.assertEqual(cm.fact(n), cm.fact_db(n), "fix factorial")

class TestFactStl2(unittest.TestCase):
    def test_fact_stl2(self):
        for i in xrange(1000):
            n = random.randint(0, 2000)
            k = random.randint(0, n)
            a = cm.fact(k) * stirling2(n, k)
            b = cm.fact_stl2(n, k)
            self.assertEquals(a, b, "good %d mine %d" % (a, b))
        
def test_main():
    test_support.run_unittest(TestFact)

if __name__ == '__main__':
    test_main()



