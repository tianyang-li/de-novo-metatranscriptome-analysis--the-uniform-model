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

def main(args):
    embl_file = None
    psl1_file = None
    psl2_file = None
    if (not embl_file
        or not psl2_file 
        or not psl1_file):
        print >> sys.stderr, "missing"
        sys.exit(1)

if __name__ == '__main__':
    main(sys.argv[1:])    

