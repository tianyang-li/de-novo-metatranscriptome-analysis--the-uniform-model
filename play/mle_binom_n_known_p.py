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

import sys
import getopt
from numpy.random import binomial as binom

def main(args):
    p, n, runs = None, None, None
    try:
        opts, args = getopt.getopt(args, 'p:n:r:')
    except getopt.GetoptError as err:
        print >> sys.stderr, str(err)
    for opt, arg in opts:
        if opt == '-p':
            p = float(arg)
        if opt == '-n':
            n = int(arg)
        if opt == '-r':
            runs = int(arg)
    if p == None or n == None or runs == None:
        print >> sys.stderr, "missing options"
        sys.exit(1)
    
    N = int(n / p)
    for i in xrange(runs):
        n_mc = binom(N, p)
        print int(n_mc / p)

if __name__ == '__main__':
    main(sys.argv[1:])



