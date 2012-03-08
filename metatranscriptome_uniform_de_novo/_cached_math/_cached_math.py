#!/usr/bin/env python

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
        

class _Binom(object):
    def __init__(self):
        # binom(n, k) = self._binom_cache[n][k]
        self._binom_cache = [[1]]

    def __call__(self, n, k):
        if k > n or n < 0 or k < 0:
            return 0
        for i in xrange(n + 1):
            if len(self._binom_cache) <= i:
                self._binom_cache.append([1])
            for j in xrange(len(self._binom_cache[i]), min(k, i) + 1):
                self._binom_cache[i].append(self._binom_cache[i - 1][j - 1])
                if j <= i - 1:
                    self._binom_cache[i][j] += self._binom_cache[i - 1][j]                
        return self._binom_cache[n][k]

class _FactorialStirling2(object):
    """
    k! * S(n, k)
    """
    def __init__(self):
        # fact_stl2(n, k) = self._factorial_stirling2_cache[n][k]
        self._factorial_stirling2_cache = []

    def __call__(self, n, k):
        if k > n:
            return 0
        #TODO

class _IntExponent(object):
    """
    n ** m (n >= 0, m >= 0) 
    0 ** 0 = 1
    """    
    def __init__(self):
        self._int_exponent_cache = [[1]]
    
    def __call__(self, n, m):
        if n == 0:
            if m == 0:
                return 1
            else:
                return 0
        #TODO

