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

from short_contig_analysis_single_0 import single_contig_calc_t_stat

from random import randint

def main():
    eff_len = 1000
    n_reads = 50
    runs = 100000
    for _ in xrange(runs):
        read_pos = [0] * eff_len
        read_pos[0] = 1
        read_pos[-1] = 1
        for _ in xrange(n_reads):
            read_pos[randint(0, eff_len - 1)] += 1
        print single_contig_calc_t_stat(read_pos, eff_len, n_reads)

if __name__ == '__main__':
    main()


