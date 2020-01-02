#!/usr/bin/env python

import sys
import xml.etree.ElementTree as ET
import shapes as shapes_pkg
from shapes import point_generator
from config import *
import re
from math import sqrt


path = "./svg/lines.svg"
path = "./svg/medium_example.svg"
#path = "./svg/text.svg"
#path = "./svg/example.svg"

debug = False
zTravel = 50

def get_shapes(path, autoScale=True):
    print("get shapes")
    svg_shapes = set(['rect', 'circle', 'ellipse', 'line', 'polyline', 'polygon', 'path'])
    shapes = []
    tree = ET.parse(path)
    root = tree.getroot()
    width = root.get('width')
    height = root.get('height')

    if width == None or height == None:
        viewbox = root.get('viewBox')
        if viewbox:
            _, _, width, height = viewbox.split()

    if width == None or height == None:
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

            # print("\n\n\n***************** elem ******************")
            # print(elem)
            # print("")
            # print(tag_suffix)
            # print("")

            shape_class = getattr(shapes_pkg, tag_suffix)
            shape_obj = shape_class(elem)
            d = shape_obj.d_path()
            m = shape_obj.transformation_matrix()  # todo work out what d and m are

            coords = []

            if d:  # begin shape processing

                p = point_generator(d, m, smoothness)  # tuples of x y coords

                first = True

                for x, y in p:  # todo sort out this nightmare

                    # print(x, y)

                    if first:
                        coords.append((x, -y+height))

                    else:

                        if not (x, y) == coords[-1]:
                            coords.append((x, -y+height))

                    if first:
                        first = False

            shapes.append(coords)

    return shapes

def g_string(x, y, z=False, prefix="G1", p=3):
    if z is not False:
        return f"{prefix} X{x:.{p}f} Y{y:.{p}f} Z{z:.{p}f}"

    else:
        return f"{prefix} X{x:.{p}f} Y{y:.{p}f}"

def shapes2gcode(shapes):

    print("shapes 2 gcode")
    commands = []
    for i in shapes:

        commands.append( g_string(i[0][0],i[0][1],zTravel,"G0"))

        for j in i:
            commands.append(g_string(j[0], j[1], zDraw))

        commands.append(g_string(i[-1][0], i[-1][1], zTravel, "G0"))

    return commands


def getDistance(a, b):
    x1, y1 = a[0], a[1]
    x2, y2 = b[0], b[1]

    x = x2 - x1
    y = y2 - y1

    return sqrt(x * x + y * y)


shapes = get_shapes(path)
c = shapes2gcode(shapes)


print("")

newOrder = []


newOrder.append(shapes.pop(0))

print("begin")
l = len(shapes)
while len(newOrder) < l:

    shortest = float("Inf")
    last = newOrder[-1][-1]
    for shape in shapes:
        d = getDistance(last, shape[0])
        if d < shortest:
            shortest = d
            selection = shape

    newOrder.append(selection)
    shapes.remove(selection)





# for i in shapes:
#     for j in shapes:



c = shapes2gcode(newOrder)

output = "./gcode_optimised/1.gcode"

if __name__ == "__main__":


    with open(output, 'w+') as output_file:
        for i in c:
            output_file.write(i + "\n")

    print("done")
