"""
lego_FreeCAD.py
Paul Cobbaut, 2022-09-23
Some FreeCAD scripting
The goal is to make nonexisting Lego-compatible pieces for use in 3D printer
For example a 30x10 studs box with flat bottom, 8 bricks high, studs all over the top side
"""


# Dimensions used
stud_radius = 2.4		# documented as 2.4 or 2.5 or 2.47
stud_center_spacing = 8.0
stud_height = 1.7		# brick_height / 3 - brick_walls_thickness

plate_height = 3.2		# stud_center_spacing * 2 / 5
plate_width = 7.8		# for 1x1 plate and 1x1 brick
gap = 0.2			# inbetween two 1x1;  X studs is X * (plate_width + gap) - gap
				# example: plate_width + gap + plate_width + gap + plate_width
brick_height = 9.6		# stud_center_spacing * 6 / 5  (or plate_height * 3)
brick_wall  = 0.75		# (stud_center_spacing - stud_diameter) / 2 / 2
brick_width = 7.8		# = plate_width

# open underside from onionrobots
#underside_cylinder_outer_diameter = 6.31
#underside_cylinder_wall_thickness = 0.657


import FreeCAD
from FreeCAD import Base, Vector
import Part
import Sketcher

# FreeCAD document
doc = FreeCAD.newDocument("Lego brick generated")
obj = doc.addObject("PartDesign::Body", "Body")

def make_prism(name, x, y, z):
    obj = doc.addObject("Part::Box", name)
    obj.Length = x
    obj.Width = y
    obj.Height = z
    doc.recompute()
    return obj

def make_stud(name):
    obj = doc.addObject("Part::Cylinder", name)
    obj.Radius = stud_radius
    obj.Height = stud_height
    doc.recompute()
    return obj

def calculate_width(y):
    w = (y * (brick_width + gap)) - gap
    return w

stud_template = make_stud("stud_template")


# create a 1x1 brick
brick1 = make_prism("brick1x1", brick_width, brick_width, brick_height)
doc.brick1x1.Placement = FreeCAD.Placement(Vector(0, 0, 0), FreeCAD.Rotation(0, 0, 0), Vector(0, 0, 0))
stud1 = make_stud("stud1x1")
doc.stud1x1.Placement = FreeCAD.Placement(Vector(0, 0, brick_height), FreeCAD.Rotation(0, 0, 0), Vector(0, 0, 0))


# create an x by y brick
x = 2
y = 6
length = calculate_width(y)
width = calculate_width(x)
prism = make_prism("prism", width, length, brick_height)
#studs = create_studs(width, length)



doc.recompute()

FreeCADGui.ActiveDocument.ActiveView.fitAll()




