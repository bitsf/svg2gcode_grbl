#!/usr/bin/env python

import sys
import xml.etree.ElementTree as ET
import shapes as shapes_pkg
from shapes import point_generator
from config import *

path = "./svg/example.svg"

#path = "./svg/big_example.svg"
#path = "./svg/medium_example.svg"
#path = "./svg/bunny.svg"

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
    commands.append("(begin)")
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

            for i in ["\n", "({})".format(tag_suffix), ""]:
                commands.append(i) # add tag name ad comment

            shape_class = getattr(shapes_pkg, tag_suffix)
            shape_obj = shape_class(elem)
            d = shape_obj.d_path()

            m = shape_obj.transformation_matrix() #todo work out what d and m are

            if debug:
                print("\nd", d)
                print(d)
                print("\nm", m)
                print(m)

            if d:  # begin shape processing
                if debug:
                    print("\nshape preamble")
                    print(shape_preamble)

                commands.append(shape_preamble)

                p = point_generator(d, m, smoothness)  # tuples of x y coords


                count = 0
                for x, y in p:

                    if count == 0:
                        first = (x,y)
                        commands.append("G0 X%0.1f Y%0.1f Z%0.1f" %(x, y, zTravel))  # todo what is %0.1f

                    # if x > 0 and x < bed_max_x and y > 0 and y < bed_max_y:
                    if debug:
                        print("G1 X%0.1f Y%0.1f" % (x, y))

                    commands.append("G1 X%0.1f Y%0.1f Z%0.1f" % (x, y, zDraw))

                    # else:
                    #     print("out of bed")
                    count += 1

                last = (x,y)
                commands.append("G0 Z%0.1f" %zTravel)

                if debug:
                    print(shape_postamble)
                commands.append(shape_postamble)

    print(postamble)
    commands.append(postamble)
    return commands


if __name__ == "__main__":
    c = generate_gcode(tree)
    # for i in c:
    #     print(i)

    with open("./gcode/output.gcode", 'w+') as output_file:
        for i in c:
            output_file.write(i + "\n")

    print("done")
