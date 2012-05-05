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
import getopt
import sys
from random import randint
from math import log

def find_one_contig_N(prob_precision, prob_one_contig, L, d_max, read_len):
    sim_runs = int(2.1910133173369407 / prob_precision ** 2) + 1
    N = int(L * log(L) / d_max) + 1
    CHANGE_RATIO = 0.75
    
    eff_len = L - read_len + 1
    
    class SingleOneContig(object):
        def __init__(self):
            self.nuc_seq = [0] * eff_len
            self.read_pos = []
            self.N = 0
        
        def one_contig(self, N1):
            if self.N > N1:
                for pos in self.read_pos[N1:self.N]:
                    self.nuc_seq[pos] -= 1
                self.N = N1
            if self.N < N1:
                for n in xrange(self.N, N1):
                    self.read_pos.append(randint(0, eff_len - 1))
                    self.nuc_seq[self.read_pos[-1]] += 1
                self.N = N1
            prev = None
            for cur in xrange(eff_len):
                if self.nuc_seq[cur] != 0:
                    if prev != None:
                        if cur - prev > d_max:
                            return False
                    prev = cur
            return True
        
        def debug_it(self):
            N_seq = reduce(lambda x, y: x + y, self.nuc_seq)
            if self.N != N_seq:
                return False
            return True
    
    sims = []
    for _ in xrange(sim_runs):
        sims.append(SingleOneContig())
    
    def calc_prob(cur_N):
        one_contig = 0
        for sim in sims:
            if sim.one_contig(cur_N):
                one_contig += 1
        return one_contig / sim_runs
    
    cur_prob = calc_prob(N)
    
    if abs(cur_prob - prob_one_contig) > prob_precision:
        N_upper, N_lower = None, None
        prob_upper, prob_lower = None, None
        
        if cur_prob > prob_one_contig:
            N_upper = N
            prob_upper = cur_prob
            N_lower = int(N * CHANGE_RATIO)
            prob_lower = calc_prob(N_lower)
            
            while prob_lower > prob_one_contig:
                N_upper = N_lower
                prob_upper = prob_lower
                N_lower = int(CHANGE_RATIO * N_lower)
                prob_lower = calc_prob(N_lower)
        else:
            N_upper = int(N / CHANGE_RATIO)
            prob_upper = calc_prob(N_upper)
            N_lower = N
            prob_lower = cur_prob
        
            while prob_upper < prob_one_contig:
                N_lower = N_upper
                prob_lower = prob_upper
                N_upper = int(N_upper / CHANGE_RATIO)
                prob_upper = calc_prob(N_upper)
                
        while ((abs(prob_upper - prob_one_contig) > prob_precision 
                or abs(prob_lower - prob_one_contig) > prob_precision)
               and N_upper - N_lower > 1):
            N_tmp = int((N_upper + N_lower) / 2)
            prob_tmp = calc_prob(N_tmp)
            if prob_tmp < prob_one_contig:
                N_lower = N_tmp
                prob_lower = prob_tmp
            else:
                N_upper = N_tmp
                prob_upper = prob_tmp
            
        return int((N_upper + N_lower) / 2)
    else:
        return N

def main(args):
    L, d_max, read_len = None, None, None
    try:
        opts, args = getopt.getopt(args, 'l:r:d:')
    except getopt.GetoptError as err:
        print >> sys.stderr, str(err)
        sys.exit(1)
    for opt, arg in opts:
        if opt == '-l':
            L = int(arg)
        if opt == '-d':
            d_max = int(arg)
        if opt == '-r':
            read_len = int(arg)
    if L == None or d_max == None or read_len == None:
        print >> sys.stderr, "missing"
        sys.exit(1)
    print find_one_contig_N(0.01, 0.95, L, d_max, read_len)
    
if __name__ == '__main__':
    main(sys.argv[1:])


