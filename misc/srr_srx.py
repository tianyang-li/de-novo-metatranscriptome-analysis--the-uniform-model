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

from xml.etree.ElementTree import ElementTree

def main(args):
    run_xml = ElementTree()
    run_xml.parse(args[0])
    run_attrib = []
    for elem in run_xml.getiterator():  # change this when using Python 2.7
        if elem.tag == "RUN":
            if len(run_attrib) == 3:
                for ra in run_attrib:
                    print ra,
                print 
            run_attrib = []
            run_attrib.append(elem.attrib["accession"])
        if elem.tag == "EXPERIMENT_REF":
            run_attrib.append(elem.attrib["accession"])
        if elem.tag == "VALUE":
            if "[tagged" in elem.text:
                run_attrib.append(elem.text.split(" ")[0])
            
    

if __name__ == '__main__':
    main(sys.argv[1:])
