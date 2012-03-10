#!/usr/bin/env python
from genericpath import isfile

# This file is part of de_novo_uniform_metatranscriptome.
# 
# de_novo_uniform_metatranscriptome is free software: 
# you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
# 
# de_novo_uniform_metatranscriptome is distributed in 
# the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
# 
# You should have received a copy of the GNU General Public License
# along with de_novo_uniform_metatranscriptome.  
# If not, see <http://www.gnu.org/licenses/>.

# Copyright (2012) Tianyang Li
# tmy1018@gmail.com

"""
mathematical functions to use during calculations

intermediate results are stored for further use
"""

import bsddb3.db as db
from os import remove
from sys import stderr

class _Factorial(object):
    def __init__(self):
        # fact(n) = self._factorial_cache[n]
        self._factorial_cache = [1]
    
    def __call__(self, n):
        if len(self._factorial_cache) <= n:
            prod = self._factorial_cache[-1]
            for i in xrange(len(self._factorial_cache), n + 1):
                prod *= i
                self._factorial_cache.append(prod)
            return prod
        else:
            return self._factorial_cache[n]


class _FactorialStirling2(object):
    """
    k! * S(n, k)
    """
    def __init__(self):
        # fact_stl2(n, k) = self._factorial_stirling2_cache[n][k]
        self._factorial_stirling2_cache = [1]
        self._max_n = 0

    def __call__(self, n, k):
        if k > n:
            return 0
        if n > self._max_n:
            for i in xrange(self._max_n + 1, n + 1):
                self._factorial_stirling2_cache.append(0)
                for j in xrange(1, i): 
                    self._factorial_stirling2_cache.append(j * (self._factorial_stirling2_cache[(i - 1) * i / 2 + j] + self._factorial_stirling2_cache[(i - 1) * i / 2 + j - 1]))
                self._factorial_stirling2_cache.append(i * self._factorial_stirling2_cache[i * (i - 1) / 2 + i - 1])
            self._max_n = n
        return self._factorial_stirling2_cache[(n + 1) * n / 2 + k]
        
        
