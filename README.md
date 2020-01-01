Forked from vishpat/svg2gcode

https://github.com/vishpat/svg2gcode


Modified to generate gcode for GRBL based pen plotter


Usage as cli:


_python convert.py source.svg destination.gcode_


There are various settings you can change in config.py. Most notably, you must set an upper and lower position for the z axis.

zTravel is the height it will move to before traveling to the next stroke

zDraw should be the height at which the pen will make contact with the paper