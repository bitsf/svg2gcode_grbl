from math import sqrt
from datetime import datetime as dt
from utils import *
import json

def get_distance(a, b, sq=False):
    x1, y1 = a[0], a[1]
    x2, y2 = b[0], b[1]

    x = x2 - x1
    y = y2 - y1

    if sq:
        return sqrt(x * x + y * y)
    else:
        return x * x + y * y


def get_total_distance(shapes):

    total_distance = 0
    last = shapes.pop(0)[-1]

    for i in shapes:
        total_distance += get_distance(i[0], last, sq=True)

    return total_distance


def optimise_path(shapes, sq=False):

    t1 = dt.now()
    new_order = []
    new_order.append(shapes.pop(0))
    l = len(shapes)
    lp = 0
    print(lp)
    while len(new_order) <= l:
        p = round((1-(len(shapes) / l))*100)
        if not p == lp:
            print(p)
            lp = p
        shortest = float("Inf")
        last = new_order[-1][-1]

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
            new_order.append(list(reversed(selection)))
            #new_order.append([x for x in reversed(selection)])

        else:
            new_order.append(selection)
        shapes.remove(selection)

    timer(t1, "optimizing       ")



    return new_order



def test_edges(shapes):

    m = get_min_max(shapes)
    xMin = m[0]
    yMin = m[1]
    xMax = m[2]
    yMax = m[3]


    boundry = [ [xMin, yMin], [xMin, yMax], [xMax, yMax], [xMax, yMin], xMin, yMin]
    return boundry

# def scale_shapes(shapes, x_scale, y_scale):
#
#     for i in shapes:
#         for j in i:
#             shapes[i][j][0] = shapes[i][j][0] * x_scale
#             shapes[i][j][1] = shapes[i][j][1] * y_scale
#
#     return shapes

# def lerp(old_min, new_min, old_max, new_max, value):
#
#     OldRange = (old_max - old_min)
#     NewRange = (new_max - new_min)
#     return (((value - old_min) * NewRange) / OldRange) + new_min

def get_min_max(shapes):

    xMin, yMin = float("inf"), float("inf")
    xMax, yMax = 0, 0

    for i in shapes:
        for j in i:
            xMin = min(xMin, j[0])
            xMax = max(xMax, j[0])
            yMin = min(yMin, j[1])
            yMax = max(yMax, j[1])

    print(f"min is {xMin}, {yMin}")
    print(f"max is {xMax}, {yMax}")

    return (xMin, yMin), (xMax, yMax)

def auto_scale(shapes,bed_x, bed_y):


    def scale(old_min_xy, old_max_xy, bed_xy, value_xy):

        offset_x = old_min_xy[0]
        offset_y = old_min_xy[1]

        old_max_offsetted_x = old_max_xy[0] - offset_x
        old_max_offsetted_y = old_max_xy[1] - offset_y

        scale_x = bed_xy[0] / old_max_offsetted_x
        scale_y = bed_xy[1] / old_max_offsetted_y
        scale = min(scale_x, scale_y)

        x = value_xy[0] - offset_x
        y = value_xy[1] - offset_y

        x *= scale
        y *= scale

        return x, y


    min_max = get_min_max(shapes)

    for x, i in enumerate(shapes):
        for y, j in enumerate(i):
            shapes[x][y] = scale(min_max[0], min_max[1], (bed_x, bed_y), shapes[x][y])

    return shapes
    #
    #
    # min_max = get_min_max(shapes)
    # old_min = min(min_max[0], min_max[1])
    # old_max = max(min_max[2], min_max[3])
    # new_min = 0
    # new_max = max(bed_x, bed_y)
    #
    # print(f"old min {old_min}")
    # print(f"old max {old_max}")
    # print(f"new_min {new_min}")
    # print(f"new_max {new_max}")
    #
    # # print(f"")
    #
    # # print(shapes)
    # for x, i in enumerate(shapes):
    #
    #     for y, j in enumerate(i):
    #         for z, k in enumerate(j):
    #             this = shapes[x][y][z]
    #             this_lerp = lerp(old_min, new_min, old_max, new_max, this)
    #             # print(f"{this:03}  -->  {this_lerp:03}")
    #             shapes[x][y][z] = this_lerp
    #
    # return shapes

def concatenate(shapes, threshold):
    print("concat")
    new_shapes = []
    new_shape = []
    for x, i in enumerate(shapes):

        current_start = shapes[x][0]
        previous_end = shapes[x-1][-1]
        current_shape = i

        if len(new_shape) == 0:
            new_shape = current_shape


        if get_distance(current_start, previous_end, True) < threshold:
            new_shape += current_shape

        else:
            new_shapes.append(new_shape)
            new_shape = []

    print(f"{len(shapes)} became {len(new_shapes)} shapes")

    return new_shapes

def compare_lines(line1, line2, threshold): #return true if lines are too similar

    count = 0

    def check(list):  #return true if all values are below threshold

        for i in list:
            # print(abs(i))
            if abs(i) >= threshold:
                # print(abs(i))
                return False

        return True

    l1_x1 = line1[0][0]
    l1_y1 = line1[0][1]
    l1_x2 = line1[1][0]
    l1_y2 = line1[1][1]

    l2_x1 = line2[0][0]
    l2_y1 = line2[0][1]
    l2_x2 = line2[1][0]
    l2_y2 = line2[1][1]

    d1 = l1_x1 - l2_x1
    d2 = l1_y1 - l2_y1
    d3 = l1_x2 - l2_x2
    d4 = l1_y2 - l2_y2

    d5 = l1_x1 - l2_x2
    d6 = l1_y1 - l2_y2
    d7 = l1_x2 - l2_x1
    d8 = l1_x2 - l2_y2

    c1 = check([d1, d2, d3, d4])
    c2 = check([d5, d6, d7, d8])

    if c1 or c2:
        return True
        count += 1

    else:
        return False


def remove_redundant_lines(shapes, threshold):
    count = 0
    first = True
    prev_points = shapes[0][0]
    prev_line = ()
    for shape in shapes:
        for points in shape:

            if first:
                first = False
                continue

            line = (prev_points, points)

            if not prev_line:

                prev_line = line
                continue
            if compare_lines(prev_line, line, threshold):
                count += 1
            prev_points = points
            prev_line = line
    print(f"redundant lines: {count}")



