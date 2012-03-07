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

class _Fact(object):
    def __init__(self):
        self._fact_cache = [1]
    
    def __call__(self, n):
        if len(self._fact_cache) <= n:
            prod = self._fact_cache[-1]
            for i in range(len(self._fact_cache), n + 1):
                prod *= i
                self._fact_cache.append(prod)
            return prod
        else:
            return self._fact_cache[n]

class _Binom(object):
    def __init__(self):
        self._binom_cache = []

    def __call__(self, n, k):
        if k > n:
            return 0
        #TODO
                

    
    

