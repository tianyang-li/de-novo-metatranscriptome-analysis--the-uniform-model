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
basic mathematical functions to use during calculations

intermediate results are stored for further use
"""

import bsddb3.db as db
from os.path import isfile
from marshal import loads, dumps


class Factorial(object):
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



class FactorialStirling2(object):
    """
    k! * S(n, k)
    """
    _cache_name = "factorial_stirling2.bsddb"
    
    # largest 
    _n_max_key = "n_max"
    
    def __init__(self):
        self._cache = db.DB()
        if isfile(self._cache_name):
            self._cache.open(self._cache_name, dbtype=db.DB_BTREE)
            self._n_max = loads(self._cache.get(self._n_max_key))
        else:
            self._cache.open(self._cache_name, dbtype=db.DB_BTREE, flags=db.DB_CREATE)
            self._n_max = 0
            self._cache.put(dumps((0, 0)), dumps(1)) 
            
    def __call__(self, n, k):
        """
        assumes that n >= 0 and k >= 0
        """
        if k > n:
            return 0
        if n > self._n_max:
            for i in xrange(self._n_max + 1, n + 1):
                self._cache.put(dumps((i, 0)), dumps(0))
                for j in xrange(1, i):
                    self._cache.put(dumps((i, j)), dumps(j * (loads(self._cache.get(dumps((i - 1, j)))) + loads(self._cache.get(dumps((i - 1, j - 1)))))))
                self._cache.put(dumps((i, i)), dumps(i * loads(self._cache.get(dumps((i - 1, i - 1))))))
            self._n_max = n
        return loads(self._cache.get(dumps((n, k))))
    
    def close(self):
        self._cache.put(self._n_max_key, dumps(self._n_max))
        self._cache.close()

class Binom(object):
    _cache_name = "binom.bsddb"
    
    # largest
    _n_max_key = "n_max"
    
    def __init__(self):
        self._cache = db.DB()
        if isfile(self._cache_name):
            self._cache.open(self._cache_name, dbtype=db.DB_BTREE)
            self._n_max = loads(self._cache.get(self._n_max_key))
        else: 
            self._cache.open(self._cache_name, dbtype=db.DB_BTREE, flags=db.DB_CREATE)
            self._n_max = 0
            self._cache.put(dumps((0, 0)), dumps(1)) 
    
    def __call__(self, n, k):
        if k > n or n < 0 or k < 0:
            return 0
        if n > self._n_max:
            for i in xrange(self._n_max + 1, n + 1):
                self._cache.put(dumps((i, 0)), dumps(1))
                for j in xrange(1, i):
                    self._cache.put(dumps((i, j)), dumps(loads(self._cache.get(dumps((i - 1, j)))) + loads(self._cache.get(dumps((i - 1, j - 1))))))
                self._cache.put(dumps((i, i)), dumps(1))
            self._n_max = n
        return loads(self._cache.get(dumps((n, k))))

    def close(self):
        self._cache.put(self._n_max_key, dumps(self._n_max))
        self._cache.close()

class IntExp(object):
    _cache_name = "int_exp.bsddb"
    
    def __init__(self):
        self._cache = db.DB()
        if isfile(self._cache_name):
            self._cache.open(self._cache_name, dbtype=db.DB_BTREE)
        else:
            self._cache.open(self._cache_name, dbtype=db.DB_BTREE, flags=db.DB_CREATE)
            
    def __call__(self, n, m):
        """
        n ** m
        
        0 ** 0 = 1
        
        assumes that n >= 0 and m >= 0
        """
        if n == 1:
            return 1
        if n == 0:
            if m == 0:
                return 1
            else:
                return 0
        # n >= 2
        
    
    def close(self):
        self._cache.close()
        
