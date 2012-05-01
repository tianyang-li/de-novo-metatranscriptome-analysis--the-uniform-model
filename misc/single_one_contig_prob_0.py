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

def single_one_contig(sim, d_max):
    prev = None
    for pos in xrange(len(sim)):
        if sim[pos] != 0:
            if prev != None:
                if pos - prev > d_max:
                    return False
            prev = pos
    return True

def main(args):
    d_max, read_len = None, None
    prob_max = None  # upper bound for simulating the probability of getting one contig
    MAX_LEN = 6000
    precision = None  # precision in probability simulation for "95% confidence interval"
    try:
        opts, args = getopt.getopt(args, 'd:l:u:p:')
    except getopt.GetoptError as err:
        print >> sys.stderr, str(err)
        sys.exit(1)
    for opt, arg in opts:
        if opt == '-l':
            read_len = int(arg)
        if opt == '-d':
            d_max = int(arg)
        if opt == '-u':
            prob_max = float(arg)
        if opt == '-p':
            precision = float(arg)
    if d_max == None or read_len == None or prob_max == None or precision == None:
        print >> sys.stderr, "missing options"
        sys.exit(1)
    N = 2
    prob1 = 0.0  # probability of getting one contig
    sim_runs = int(2.1910133173369407 / precision ** 2) + 1
    sims = []
    eff_len = MAX_LEN - read_len + 1
    for r in xrange(sim_runs):
        sims.append([0] * eff_len)
    for sim in sims:
        sim[randint(0, eff_len - 1)] += 1
    while prob1 < prob_max:
        for sim in sims:
            sim[randint(0, eff_len - 1)] += 1
        one_contig = 0
        for sim in sims:
            if single_one_contig(sim, d_max):
                one_contig += 1
        prob1 = one_contig / sim_runs
        print "%d,%.15f" % (N, prob1)
        N += 1

if __name__ == '__main__':
    main(sys.argv[1:])


