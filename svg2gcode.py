#!/usr/bin/env python

import sys
import xml.etree.ElementTree as ET
import shapes as shapes_pkg
from shapes import point_generator
from config import *

path = "./svg/example.svg"
path = "./svg/big_example.svg"
tree = ET.parse(path)

debug = False


def generate_gcode(tree):
    svg_shapes = set(['rect', 'circle', 'ellipse', 'line', 'polyline', 'polygon', 'path'])

    commands = []

    # tree = ET.parse(sys.stdin)
    root = tree.getroot()

    # print("\n printing root.iter")
    # for i in root.iter():
    #     print(i.tag)
    #
    # print("\n printing root with tag and attrib")
    # for i in root:
    #     print(i.tag, i.attrib)

    width = root.get('width')
    height = root.get('height')



    if width == None or height == None:
        viewbox = root.get('viewBox')
        if viewbox:
            _, _, width, height = viewbox.split()                

    if width == None or height == None:
        print("Unable to get width and height for the svg")
        sys.exit(1)


    print("\n width / height")
    print(width, height)

    width = float(width)
    height = float(height)

    scale_x = bed_max_x / max(width, height)
    scale_y = bed_max_y / max(width, height)

    print("\npreamble")
    print(preamble)
    commands.append(preamble)

    print("\n begin main loop")

    for elem in root.iter():

        if debug:
            print("\nelem")
            print(elem)

        try:
            _, tag_suffix = elem.tag.split('}')
        except ValueError:
            continue


        if tag_suffix in svg_shapes:

            if debug:
                print("\ntag_suffix")
                print(tag_suffix)

            shape_class = getattr(shapes_pkg, tag_suffix)
            shape_obj = shape_class(elem)
            d = shape_obj.d_path()
            m = shape_obj.transformation_matrix()

            if d:
                if debug:
                    print("\nshape preamble")
                    print(shape_preamble)
                commands.append(shape_preamble)
                p = point_generator(d, m, smoothness)
                # print("\npoint_generator\n", p)
                # for i in p:
                #     print(i)
                for x,y in p:
                    #if x > 0 and x < bed_max_x and y > 0 and y < bed_max_y:
                    if debug:
                        print("G1 X%0.1f Y%0.1f" % (scale_x*x, scale_y*y))
                    commands.append("G1 X%0.1f Y%0.1f" % (scale_x*x, scale_y*y))

                    # else:
                    #     print("out of bed")

                if debug:
                    print(shape_postamble)
                commands.append(shape_postamble)


    print(postamble)
    commands.append(postamble)
    return commands

if __name__ == "__main__":
    c = generate_gcode(tree)
    for i in c:
        print(i)



