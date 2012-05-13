#!/usr/bin/env python

import short_contig_analysis_0

def main():
    a = [2, 0, 0, 0, 3]
    print short_contig_analysis_0.calc_t_stat(a, len(a), reduce(lambda x, y:x + y, a))

if __name__ == '__main__':
    main()

