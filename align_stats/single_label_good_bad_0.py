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

def keep_contig(est_len, true_len, reb, aeb):
    """
    reb - relative error bound
    aeb - absolute error bound
    """
    if (abs(est_len - true_len) <= aeb
        or abs(est_len - true_len) / true_len <= reb):
        return True
    return False

def main(args):
    """
    this is the output i have
    
    0  contig.low
    1  contig.high - contig.low + 1
    2  est_len
    3  found_iv.type
    4  found_iv.low
    5  found_iv.high - found_iv.low + 1
    6  coverage median
    7  coverage max
    8  coverage list
    9  overlap_type
    """
    rel_err_bnd = None # relative error in estimation bounds
    abs_err_bnd = None # absolute error bound
    """
    contigs satisfying
        rel_err <= rel_err_bnd or abs_err <= abs_err_bnd
    will be labled as good
    otherwise bad 
    """
    try:
        opts, args = getopt.getopt(args, 'i:r:a:p:')
    except getopt.GetoptError as err:
        print >> sys.stderr, str(err)
        sys.exit(1)
    contig_info = None
    out_prefix = None
    
    for opt, arg in opts:
        if opt == '-i':
            contig_info = arg
        if opt == '-r':
            rel_err_bnd = float(arg)
        if opt == '-a':
            abs_err_bnd = float(arg)
        if opt == '-p':
            out_prefix = arg
            
    if (not rel_err_bnd
        or not out_prefix
        or not abs_err_bnd
        or not contig_info):
        print >> sys.stderr, "missing"
        sys.exit(1)
    
    good_out = open("%s_good" % out_prefix, 'w')
    bad_out = open("%s_bad" % out_prefix, 'w')
    
    good_out.close()
    bad_out.close()

if __name__ == '__main__':
    main(sys.argv[1:])    
    
    
    
