#!/usr/bin/env python

#  Copyright (C) 2012 Tianyang Li
#  tmy1018@gmail.com
#
#  This program is free software: you can redistribute it and/or modify
#  it under the terms of the GNU General Public License as published by
#  the Free Software Foundation, either version 3 of the License, or
#  (at your option) any later version.
#
#  This program is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#  GNU General Public License for more details.
#
#  You should have received a copy of the GNU General Public License

from random import randint

def select(a, k):
    """
    assumes 
        1 <= k <= len(a)
    """
    # 0 based, inclusive
    def partition(low, high, piv):
        piv_val = a[piv]
        a[high], a[piv] = a[piv], a[high]
        piv = low
        for cur_pos in xrange(low, high):
            if a[cur_pos] <= piv_val:
                a[piv], a[cur_pos] = a[cur_pos], a[piv]
                piv += 1
        a[piv], a[high] = a[high], a[piv]
        return piv
    
    cur_low = 0
    cur_high = len(a) - 1
    
    while cur_low <= cur_high:
        piv = randint(cur_low, cur_high)
        piv = partition(cur_low, cur_high, piv)
        piv_dist = piv - cur_low + 1
        if piv_dist == k:
            return a[piv]
        elif piv_dist > k:
            cur_high = piv - 1
        else:
            k -= piv_dist
            cur_low = piv + 1
    
        
