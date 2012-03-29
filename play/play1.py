#!/usr/bin/env python

"""

print log of max of 

n! \frac{\binom{N}{n}}{L^N} \sum_{i=0}^{L-c-1} (L-c-1-\min(i,d)-\min(L-c-1-i,d))^{N-n}

when L is fixed for L in the range [c+1, 2c+d+2]
"""

from __future__ import division
import getopt
import sys
from math import log

def main(args):
    c, n, d = None, None, None
    try:
        opts, args = getopt.getopt(args, 'c:n:d:')
    except getopt.GetoptError as err:
        print >> sys.stderr, str(err)
        sys.exit(1)
    for opt, arg in opts:
        if opt == '-c':
            c = int(arg)
        if opt == '-n':
            n = int(arg)
        if opt == '-d':
            d = int(arg)
    if c == None or n == None or d == None:
        print >> sys.stderr, "missing options"
        sys.exit(1)
    
    for L in xrange(c + d + 2, 2 * c + d + 2):
        print L,
        N_opt, log_lh = None, None
        N_min = int(n * L / (c + 1 + d + min(d, L - c - d - 1)))
        for N in xrange(N_min, int(n * L / (c + 1 + d)) + 1):
            lh = -N * log(L)
            for n_comb in xrange(N - n + 1, N + 1):
                lh += log(n_comb)
            tmp_cnt = 0
            pos_pos = L - c - 2 * d - 1
            if pos_pos > 0:
                tmp_cnt += (pos_pos + 1) * ((pos_pos) ** (N - n))
            for d_tmp in xrange(d):
                pos_pos = L - c - d - d_tmp - 1
                if pos_pos > 0:
                    tmp_cnt += (2 * ((pos_pos) ** (N - n)))
            lh += log(tmp_cnt)
            if log_lh == None:
                N_opt = N
                log_lh = lh
            else:
                if lh > log_lh:
                    N_opt = N
                    log_lh = lh
        print N_opt, log_lh

if __name__ == '__main__':
    main(sys.argv[1:])





