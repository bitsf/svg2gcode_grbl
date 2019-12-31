"""G-code emitted at the start of processing the SVG file"""
preamble = "(preamble)"
#preamble = "G1 X0, Y0, Z100"


"""G-code emitted at the end of processing the SVG file"""
postamble = "(postamble)"

"""G-code emitted before processing a SVG shape"""
shape_preamble = "(shape preamble)"
#shape_preamble = "Z0"

"""G-code emitted after processing a SVG shape"""
shape_postamble = "(shape postamble)"
#shape_postamble = "Z100)"

"""Print bed width in mm"""
bed_max_x = 200000

"""Print bed height in mm"""
bed_max_y = 200000

""" 
Used to control the smoothness/sharpness of the curves.
Smaller the value greater the sharpness. Make sure the
value is greater than 0.1
"""
smoothness = 10



zTravel = 100

zDraw = 0

