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

from _cached_math import fact

def fact_stl2(n, k):
    """
    k! S(n, k)
    """
    if n < k or n < 0 or k < 0:
        return 0
    prev = [1]
    for i in xrange(1, n + 1):
        cur = [0]
        for j in xrange(1, min(k, i)):
            cur.append(j * (prev[j] + prev[j - 1]))
        if k >= i:
            cur.append(i * prev[i - 1])
        else:
            cur.append(k * (prev[k] + prev[k - 1]))
        prev = cur
    return prev[k]
