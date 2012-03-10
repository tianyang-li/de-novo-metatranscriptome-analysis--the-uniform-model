#!/usr/bin/env python

import random
import unittest
from test import test_support

import metatranscriptome_uniform_de_novo._cached_math as cm
import metatranscriptome_uniform_de_novo._math as rm

class TestFactStl2(unittest.TestCase):
    def test_fact_stl2(self):
        for i in xrange(1000):
            n = random.randint(0, 1000)
            k = random.randint(0, n)
            a = cm.fact_stl2(n, k)
            b = cm.fact_stl2(n, k)
            self.assertEqual(a, b, "fix simple version")
            
            
            
def test_main():
    test_support.run_unittest(TestFactStl2)

if __name__=='__main__':
    test_main()


