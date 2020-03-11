from optimise import optimise_path
from svg2gcode import get_shapes, shapes_2_gcode
from os.path import join
from json import dump as jdump, load as jload
from utils import *

# def write(output_file_name, data):
#     with open(output_file_name, 'w+') as output_file:
#         output_file.write(data)

def dump(outfile, data):
    with open(outfile, 'w+') as o:
        jdump(data, o)


def read(infile):
    with open(infile) as i:
        return jload(i)

proj_location = "/Users/alexanderharding/Dropbox/bish/project/plots/rofl/square"
file_location = join(proj_location, "svg")

print(file_location)

svg_file = "round_1.svg"
svg_file = "text.svg"
shapes_output = f"{svg_file}.json"
optimised_output = f"{svg_file}_optimised.json"
gcode_output = "dun.gcode"

auto_scale = False
#
# shapes = get_shapes(join(file_location, svg_file), auto_scale)    #parse svg
# dump(join(file_location, shapes_output), shapes)                  #dump parsed svg to json
# jshapes  = (read(join(file_location, shapes_output)))               #read shapes from json
# new_order = optimise_path(jshapes)                                  #optimise json shapes
# dump(join(file_location, optimised_output), new_order)              #dunmp optimised shapes
#
# # jnew_order = read(join(file_location,optimised_output))           #read optimised shapes
# # commands = shapes_2_gcode(jnew_order)                             #generate gcode commands
#
# # write_gcode(join(file_location, gcode_output), commands)          #write gcode file
