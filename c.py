#!/usr/bin/env python

from svg2gcode import generate_gcode
import sys
import os
# from config import *

if __name__ == "__main__":


    if len(sys.argv) < 4:
        print("usage: python s2g source.svg destination.gcode")
        sys.exit()

    sourceDir = sys.argv[1]
    sourceFile = sys.argv[2]
    targetFile = sys.argv[3]

    source = os.path.join(sourceDir, sourceFile)
    target = os.path.join(sourceDir, targetFile)


    print("converting!")

    print(source, target)

    with open(target, 'w+') as output_file:
        g = generate_gcode(source)
        for i in g:
            output_file.write(i + "\n")

    print("done!")
