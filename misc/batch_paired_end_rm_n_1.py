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

import sys
from itertools import izip

import kick_n

def main(args):
    for seq1, seq2 in izip(args[::2], args[1::2]):
        pseudo_args = ["-f", "fastq", "-p", "%s-noN" % seq1[:-8], "-1", seq1, "-2", seq2]
        kick_n.main(pseudo_args)
    
if __name__ == '__main__':
    main(sys.argv[1:])


