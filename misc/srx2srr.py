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
import getopt
 
def main(args):
    info = None
    try:
        opts, args = getopt.getopt(args, 'i:')
    except getopt.GetoptError as err:
        print >> sys.stderr, str(err)
        sys.exit(1)
    for opt, arg in opts:
        if opt == '-i':
            info = arg
    if info == None:
        print >> sys.stderr, "missin opts"
        sys.exit(1)
    srxs = {}
    with open(info, 'r') as fin:
        for line in fin:
            entries = line.strip().split(" ")
            if entries[1] in srxs:
                srxs[entries[1]].append(entries[0])
            else:
                srxs[entries[1]] = [entries[0]]
    for srx in args:
        for srr in  srxs[srx]:
            print srr,
    
if __name__ == '__main__':
    main(sys.argv[1:])

