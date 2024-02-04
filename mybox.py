"""
mybox.py -- Paul Cobbaut, 2024-02-04
Create a box that should be completed with panels
A 60cm by 32cm by 32cm rectangular box. Buy the panels, 3D-print the rest.
Use Part Workbench scripting in FreeCAD
"""

# Dimensions
x_mm = 600
y_mm = 320
z_mm = 320
wall_mm = 20  # thickness of the walls (in fact the beams)

# The directory to export the .stl files to
export_directory = "/home/paul/FreeCAD_generated/mybox/"

import FreeCAD
from FreeCAD import Base, Vector
import Part
import Mesh
import math

doc = FreeCAD.newDocument("Mybox generated")

def create_cube(name, x, y, z, posx, posy, posz):
    obj        = doc.addObject("Part::Box","Box")
    obj.Label  = name
    obj.Length = x
    obj.Width  = y
    obj.Height = z
    obj.Placement = FreeCAD.Placement(Vector(posx, posy, posz),FreeCAD.Rotation(Vector(0,0,1),0))
    return obj


# create beam structure with panel grooves by substracting cubes
# CompleteBox contains everything
name = 'CompleteBox'
x = x_mm
y = y_mm
z = z_mm
posx = 0
posy = 0
posz = 0
CompleteBox = create_cube(name, x, y, z, posx, posy, posz)
# Cut the inner parts and the stuff between the beams
# by creating three inner boxes each one too wide in its dimension
name = 'XBox'
x = x_mm 
y = y_mm - wall_mm
z = z_mm - wall_mm
posx = 0
posy = wall_mm/2
posz = wall_mm/2
XBox = create_cube(name, x, y, z, posx, posy, posz)
name = 'YBox'
x = x_mm - wall_mm
y = y_mm 
z = z_mm - wall_mm
posx = wall_mm/2
posy = 0
posz = wall_mm/2
YBox = create_cube(name, x, y, z, posx, posy, posz)
name = 'ZBox'
x = x_mm - wall_mm
y = y_mm - wall_mm
z = z_mm 
posx = wall_mm/2
posy = wall_mm/2
posz = 0
ZBox = create_cube(name, x, y, z, posx, posy, posz)
# Cut the three boxes from the complete box, only the beams remain
xcut = doc.addObject('Part::Cut', "xcut")
xcut.Base = CompleteBox
xcut.Tool = XBox
xcut.Label = "xcut"
ycut = doc.addObject('Part::Cut', "ycut")
ycut.Base = xcut
ycut.Tool = YBox
ycut.Label = "ycut"
frame = doc.addObject('Part::Cut', "frame")
frame.Base = ycut
frame.Tool = ZBox
frame.Label = "frame"


doc.recompute()
FreeCADGui.ActiveDocument.ActiveView.fitAll()
