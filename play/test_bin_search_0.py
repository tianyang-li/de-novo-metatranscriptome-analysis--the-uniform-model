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

from __future__ import division

import sys
import getopt

from random import randint

def bin_search(target, query):
    upper = len(target)
    lower = 0
    x = int((upper - 1 + lower) / 2)
    while upper > lower + 1 and target[x] != query:
        if target[x] > query:
            upper = x
            x = int((upper - 1 + lower) / 2)
        else:
            lower = x + 1
            x = int((upper - 1 + lower) / 2)
    if target[x] != query:
        return None
    return target[x]

def main(args):
    n = None
    runs = None
    try:
        opts, args = getopt.getopt(args, 'n:r:')
    except getopt.GetoptError as err:
        print >> sys.stderr, str(err)
        sys.exit(1)
    for opt, arg in opts:
        if opt == '-n':
            n = int(arg)
        if opt == '-r':
            runs = int(arg)
    if not n or not runs:
        print >> sys.stderr, "missing"
        sys.exit(1)
    
    test = range(n)
    for _ in xrange(runs):
        rand_q = randint(0, 2 * n - 1)
        if rand_q < n:
            if rand_q != bin_search(test, rand_q):
                print "error!"
        else:
            if bin_search(test, rand_q):
                print "error!"
    
if __name__ == '__main__':
    main(sys.argv[1:])    

