#!/usr/bin/env python

from svg2gcode import generate_gcode
import sys
# from config import *





if __name__ == "__main__":


    if len(sys.argv) < 3:
        print("usage: python convert.py source.svg destination.gcode")
        sys.exit()

    source = sys.argv[1]
    target = sys.argv[2]



    print("converting!")

    print(source, target)

    with open(target, 'w+') as output_file:
        g = generate_gcode(source)
        for i in g:
            output_file.write(i + "\n")

    print("done!")