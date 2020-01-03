#!/usr/bin/env python

import sys
import xml.etree.ElementTree as ET
import shapes as shapes_pkg
from shapes import point_generator
from config import *
import re
from math import sqrt
from datetime import datetime as dt

debug = False

def get_shapes(path, autoScale=True):
    print("\n  get shapes")
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

    timer(t1, "parsing gcode")

    return shapes


def g_string(x, y, z=False, prefix="G1", p=3):
    if z is not False:
        return f"{prefix} X{x:.{p}f} Y{y:.{p}f} Z{z:.{p}f}"

    else:
        return f"{prefix} X{x:.{p}f} Y{y:.{p}f}"


def shapes_2_gcode(shapes):
    print(" shapes 2 gcode")
    t1 = dt.now()
    commands = []
    for i in shapes:

        commands.append(g_string(i[0][0], i[0][1], zTravel, "G0"))

        for j in i:
            commands.append(g_string(j[0], j[1], zDraw))

        commands.append(g_string(i[-1][0], i[-1][1], zTravel, "G0"))

    timer(t1, "shapes_2_gcode")
    return commands


def get_distance(a, b, sq=True):
    x1, y1 = a[0], a[1]
    x2, y2 = b[0], b[1]

    x = x2 - x1
    y = y2 - y1
    if sq:
        return sqrt(x * x + y * y)
    else:
        return x * x + y * y


def timer(t, label):
    duration = dt.now() - t
    duration = duration.total_seconds()
    print("{} took {}".format(label, duration))
    return duration


def optimise_path(shapes, sq=True):
    newOrder = []
    newOrder.append(shapes.pop(0))
    l = len(shapes)
    while len(newOrder) <= l:

        shortest = float("Inf")
        last = newOrder[-1][-1]

        for shape in shapes:

            d = get_distance(last, shape[0], sq)
            d2 = get_distance(last, shape[-1], sq)

            if d < shortest:
                shortest = d
                selection = shape
                reverse = False

            if d2 < shortest:
                shortest = d2
                reverse = True
                selection = shape

        if reverse:
            newOrder.append([x for x in reversed(selection)])
        else:
            newOrder.append(selection)
        shapes.remove(selection)


if __name__ == "__main__":

    file_path = "./svg/lines.svg"
    file_path = "./svg/medium_example.svg"
    file_path = "./svg/text.svg"
    file_path = "./svg/example.svg"

    output = "./gcode_optimised/1.gcode"

    shapes = get_shapes(file_path)

    if optimize:

        newOrder = optimise_path(shapes)
        commands = shapes_2_gcode(newOrder)

    else:

        commands = shapes_2_gcode(shapes)

    with open(output, 'w+') as output_file:
        for i in c:
            output_file.write(i + "\n")

    print("done")
