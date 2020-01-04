#!/usr/bin/env python

import sys
import xml.etree.ElementTree as ET
import shapes as shapes_pkg
from shapes import point_generator
from config import *
import re
from datetime import datetime as dt
from optimise import optimise_path, get_total_distance
from utils import *

debug = False

# todo add manual scale option
# todo add z rise option
# todo why do i need to flip?

def get_shapes(path, autoScale=True):

    t1 = dt.now()
    svg_shapes = set(['rect', 'circle', 'ellipse', 'line', 'polyline', 'polygon', 'path'])
    shapes = []
    tree = ET.parse(path)
    root = tree.getroot()
    width = root.get('width')
    height = root.get('height')

    if width is None or height is None:
        viewbox = root.get('viewBox')
        if viewbox:
            _, _, width, height = viewbox.split()

    if width is None or height is None:
        print("Unable to get width and height for the svg")
        sys.exit(1)

    width = float(re.sub("[^0-9]", "", width))
    height = float(re.sub("[^0-9]", "", height))

    for elem in root.iter():

        try:
            _, tag_suffix = elem.tag.split('}')

        except ValueError:
            continue

        if tag_suffix in svg_shapes:

            shape_class = getattr(shapes_pkg, tag_suffix)
            shape_obj = shape_class(elem)
            d = shape_obj.d_path()
            m = shape_obj.transformation_matrix()  # todo work out what d and m are

            coords = []

            if d:  # begin shape processing

                p = point_generator(d, m, smoothness)  # tuples of x y coords
                first = True

                for x, y in p:  # todo sort out this nightmare

                    if first:
                        coords.append((x, -y + height))

                    else:

                        if not (x, y) == coords[-1]:
                            coords.append((x, -y + height))

                    if first:
                        first = False

            shapes.append(coords)

    timer(t1, "parsing gcode    ")

    return shapes


def g_string(x, y, z=False, prefix="G1", p=3):
    if z is not False:
        return f"{prefix} X{x:.{p}f} Y{y:.{p}f} Z{z:.{p}f}"

    else:
        return f"{prefix} X{x:.{p}f} Y{y:.{p}f}"


def shapes_2_gcode(shapes):

    t1 = dt.now()
    commands = []
    for i in shapes:

        commands.append(g_string(i[0][0], i[0][1], zTravel, "G0"))

        for j in i:
            commands.append(g_string(j[0], j[1], zDraw))

        commands.append(g_string(i[-1][0], i[-1][1], zTravel, "G0"))

    timer(t1, "shapes_2_gcode   ")
    return commands

def write_file(output, commands):

    t1 = dt.now()
    with open(output, 'w+') as output_file:
        for i in commands:
            output_file.write(i + "\n")
    timer(t1, "writing file     ")

def main(file_path, output):

    shapes = get_shapes(file_path)



    if optimise:

        pre_distance = get_total_distance(shapes)

        print("unoptimised distance: ", get_total_distance(shapes))

        new_order = optimise_path(shapes)

        post_distance = get_total_distance(new_order)

        print("unoptimised distance: ", pre_distance)
        print("optimised distance    ", post_distance)
        print("factor:               ", post_distance / pre_distance)

        commands = shapes_2_gcode(new_order)



    else:

        commands = shapes_2_gcode(shapes)

    write_file(output, commands)

    print("done")


if __name__ == "__main__":

    # file_path = "./svg/lines.svg"
    # file_path = "./svg/medium_example.svg"
    file_path = "./svg/text.svg"
    # file_path = "./svg/example.svg"

    output = "./gcode_optimised/1.gcode"

    main(file_path, output)


