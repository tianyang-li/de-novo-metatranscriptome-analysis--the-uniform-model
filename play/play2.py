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

from __future__ import division
import getopt
import sys
from math import log
from scipy.misc import comb

def main(args):
    a, n = None, None
    try:
        opts, args = getopt.getopt(args, 'a:n:')
    except getopt.GetoptError as err:
        print >> sys.stderr, str(err)
    for opt, arg in opts:
        if opt == '-a':
            a = int(arg)
        if opt == '-n':
            n = int(arg)
    if a == None or n == None :
        print >> sys.stderr, "missing options"
        sys.exit(1)
    for L in xrange(a + 1, 2 * (a + 1) + 1):
        N = int(n * L / a)
        print L, N, log(comb(N, n, exact=1)) + log(L - a) - N * log(L)

if __name__ == '__main__':
    main(sys.argv[1:])



