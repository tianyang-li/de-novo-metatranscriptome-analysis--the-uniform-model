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
math functions with no cache
"""

from os.path import isfile
import bsddb3.db as db

from .._cached_math import fact, binom, fact_stl2
 
class RestrictIntEq(object):
    _cache_name = "restrict_int_eq.bsddb"
    
    def __init__(self):
        self._cache = db.DB()
        if isfile(self._cache_name):
            self._cache.open(self._cache_name, db.DB_BTREE)
        else:
            self._cache.open(self._cache_name, db.DB_BTREE, flags=db.DB_CREATE)
            
    def __call__(self, n, m, d):
        """
        # of integer solutions
        
        x_1 + x_2 + ... + x_n = m
        
        0 < x_i <= d
        """
        
    
    def close(self):
        self._cache.close()



