#!/usr/bin/env python

import sys

def main(args):
    with open(args[0]) as fin:
        for line in fin:
            line = line.strip().split(" ")
            if line[-1] == "1" and int(line[5]) <= 6000 and int(line[7]) < 50:
                print line[2],  # est
                print line[5],  # true
                print int(line[6]) * int (line[7]), 
                print line[6],  # median
                print line[7],  # max
                print

if __name__ == '__main__':
    main(sys.argv[1:])

