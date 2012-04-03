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

import getopt
import sys
import random

def rand_cont(L, N, d):
    sim_res = [L * [0], []]
    for i in xrange(N):
        sim_res[0][random.randint(0, L - 1)] += 1
    prev_pos = None
    c, n = 0, 0
    for cur_pos in xrange(len(sim_res[0])):
        if sim_res[0][cur_pos] > 0:
            if prev_pos != None:
                if cur_pos - prev_pos > d:
                    sim_res[1].append((c, n))
                    c, n = 0, 0
                else:
                    c += (cur_pos - prev_pos)
                    n += sim_res[0][cur_pos]
            else:
                n = sim_res[0][cur_pos]
            prev_pos = cur_pos
    if n != 0:
        sim_res[1].append((c, n))
    return sim_res

def main(args):
    L, N, runs, d = None, None, None, None
    try:
        opts, args = getopt.getopt(args, 'L:N:r:d:')
    except getopt.GetoptError as err:
        print >> sys.stderr, str(err)
        sys.exit(1)
    for opt, arg in opts:
        if opt == '-L':
            L = int(arg)
        if opt == '-N':
            N = int(arg)
        if opt == '-r':
            runs = int(arg)
        if opt == '-d':
            d = int(arg)
    if L == None or N == None or runs == None or d == None:
        print >> sys.stderr, "missing options"
        sys.exit(1)
    
    random.seed()
    
    for r in xrange(runs):
        for c, n in rand_cont(L, N, d)[1]:
            print c, n

if __name__ == '__main__':
    main(sys.argv[1:])



