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

import getopt
import sys

def main(args):
    single = None
    paired = None
    frag_mean = None
    frag_std_dev = None
    d_min = None
    try:
        opts, args = getopt.getopt(args, 's:p:d:', ['mean=', 'std-dev='])
    except getopt.GetoptError as err:
        print >> sys.stderr, str(err)
        sys.exit(1)
    for opt, arg in opts:
        if opt == '-s':
            single = True
        if opt == '-p':
            paired = True
        if opt == '-d':
            d_min = int(arg)
        if opt == '--mean':
            frag_mean = float(arg)
        if opt == '--std-dev':
            frag_std_dev = float(arg)
    if single == None or paired == None or (single == True and paired == True):
        print >> sys.stderr, "simulation type error"
        sys.exit(1)
    if d_min == None:
        print >> sys.stderr, "missing d_min"
        sys.exit(1)
    if paired == True and (frag_mean == None or frag_std_dev == None):
        print >> sys.stderr, "missing parameters for fragment length"
        sys.exit(1)
    
if __name__ == '__main__':
    main(sys.argv[1:])

