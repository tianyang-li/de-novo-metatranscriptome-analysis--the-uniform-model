#!/usr/bin/env python

# Copyright (C) 2011 Tianyang Li
# tmy1018@gmail.com
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License

import sys
import getopt

def main(args):
    ids = None
    try:
        opts, args = getopt.getopt(args, 'i:')
    except getopt.GetoptError as err:
        print >> sys.stderr, str(err)
        sys.exit(1)
    for opt, arg in opts:
        if opt == '-i':
            ids = arg
    if ids == None or args == None:
        print >> sys.stderr, "missing options or arguments"
        sys.exit(1)
    for fin in args:
        with open(fin, 'r') as b6:
            for line in b6:
                entries = line.strip().split("\t")
                print entries[0].split(" ")[0], entries[1]
    
if __name__ == '__main__':
    main(sys.argv[1:])




