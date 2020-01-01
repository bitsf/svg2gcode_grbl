#!/usr/bin/env python

import sys
import xml.etree.ElementTree as ET
import shapes as shapes_pkg
from shapes import point_generator
from config import *
import re

path = "./svg/example.svg"

# path = "./svg/big_example.svg"
# path = "./svg/medium_example.svg"
# path = "./svg/bunny.svg"
# path = "./svg/grid.svg"
# path = "./svg/Lorenz_attractor.svg"
# path = "./svg/text.svg"


output = "./gcode/output.gcode"

debug = False


# todo why is it flipped?
# todo add manual scale option
# todo add propper header
# todo add z rise option
# todo make interface


def generate_gcode(path):
    svg_shapes = set(['rect', 'circle', 'ellipse', 'line', 'polyline', 'polygon', 'path'])
    precision = 1

    commands = []

    tree = ET.parse(path)
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

    width = re.sub("[^0-9]", "", width)
    height = re.sub("[^0-9]", "", height)
    print("\n width / height")
    print(width, height)

    width = float(width)
    height = float(height)

    # scale_x = bed_max_x / max(width, height)
    # scale_y = bed_max_y / max(width, height)
    # scale_x= min(scale_x, scale_y)
    # scale_y = scale_x
    #
    scale_x = 1
    scale_y = 1

    print("\npreamble")
    print(preamble)
    commands.append(preamble)
    commands.append("(begin)")
    for i in [f"{feed_rate}", "G90"]:
        commands.append(i)
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
                commands.append(i)  # add tag name ad comment

            shape_class = getattr(shapes_pkg, tag_suffix)
            shape_obj = shape_class(elem)
            d = shape_obj.d_path()

            m = shape_obj.transformation_matrix()  # todo work out what d and m are

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

                first = True
                for x, y in p:

                    if first:
                        first = (x, y)
                        # commands.append("G0 X%0.1f Y%0.1f Z%0.1f" %(scale_x*x, scale_y*y, zTravel))
                        command = g_string(x, y, zTravel, "G0", precision)
                        commands.append(command)
                        first = False

                    # if x > 0 and x < bed_max_x and y > 0 and y < bed_max_y:

                    # commands.append("G1 X%0.3f Y%0.3f Z%0.3f" % (scale_x*x, scale_y*y, zDraw))
                    command = g_string(x, y, zDraw, "G1", precision)
                    commands.append(command)
                    # else:
                    #     print("out of bed")

                    # count += 1

                # commands.append("G0 Z%0.1f" %zTravel)
                command = g_string(x, y, zTravel, "G0", precision)
                commands.append(command)

                if debug:
                    print(shape_postamble)
                commands.append(shape_postamble)

    print(postamble)
    commands.append(postamble)
    return commands


def g_string(x, y, z=False, prefix="G1", p=3):
    if z is not False:
        return f"{prefix} X{x:.{p}f} Y{y:.{p}f} Z{z:.{p}f}"

    else:
        return f"{prefix} X{x:.{p}f} Y{y:.{p}f}"


if __name__ == "__main__":
    c = generate_gcode(path)
    # for i in c:
    #     print(i)

    with open(output, 'w+') as output_file:
        for i in c:
            output_file.write(i + "\n")

    print("done")
