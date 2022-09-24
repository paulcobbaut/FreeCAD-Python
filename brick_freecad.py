"""
brick_FreeCAD.py -- Paul Cobbaut, 2022-09-23
The goal is to make nonexisting Lego-compatible pieces for use in 3D printer
For example a 30x10 studs box with flat bottom, 8 bricks high, studs all over the top side
"""
# Dimensions used
stud_radius = 2.47		# documented as 2.4 or 2.5 or 2.47
stud_center_spacing = 8.0
stud_height = 1.7		# brick_height / 3 - brick_walls_thickness

plate_height = 3.2		# stud_center_spacing * 2 / 5
plate_width = 7.8		# for 1x1 plate and 1x1 brick
gap = 0.2			# inbetween two 1x1;  X studs is X * (plate_width + gap) - gap
				# example: plate_width + gap + plate_width + gap + plate_width
brick_height = 9.6		# stud_center_spacing * 6 / 5  (or plate_height * 3)
brick_wall  = 0.75		# (stud_center_spacing - stud_diameter) / 2 / 2
brick_width = 7.8		# = plate_width

import FreeCAD
from FreeCAD import Base, Vector
import Part
import Sketcher
import Mesh

# FreeCAD document
doc = FreeCAD.newDocument("Lego brick generated")
obj = doc.addObject("PartDesign::Body", "Body")

def calculate_width(y):
    w = (y * (brick_width + gap)) - gap
    return w

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

stud_template = make_stud("stud_template")
stud_template.ViewObject.hide()

def create_studs(name, x, y, z):
    for i in range(int(x)):
        for j in range(int(y)):
            obj = doc.addObject('Part::Feature','stud_template')
            obj.Shape = doc.stud_template.Shape
            obj.Label = name + str(i) + '__' + str(j)
            xpos = ((i+1) * stud_center_spacing) - (stud_center_spacing / 2)
            ypos = ((j+1) * stud_center_spacing) - (stud_center_spacing / 2)
            obj.Placement = FreeCAD.Placement(Vector(xpos, ypos, z), FreeCAD.Rotation(0,0,0), Vector(0,0,0))
            compound_list.append(obj)

def create_a_brick(brickname, xstuds, ystuds):
    width = calculate_width(xstuds)
    length = calculate_width(ystuds)
    prism = make_prism("prism", width, length, brick_height)
    compound_list.append(prism)
    studs = create_studs("studs", xstuds, ystuds, brick_height)
    obj = doc.addObject("Part::Compound", brickname)
    obj.Links = compound_list
    return obj

def create_a_hole(brickname, xstuds, ystuds):
    obj = create_a_brick(brickname, xstuds, ystuds)
    obj.Label = brickname
    obj.Placement = FreeCAD.Placement(Vector(brick_width + gap, brick_width + gap, 0), FreeCAD.Rotation(0,0,0), Vector(0,0,0))
    return obj    


global compound_list
compound_list = []
brick55 = create_a_brick("brick55", 5, 5)
compound_list = []
hole33 = create_a_hole("hole33", 3, 3)

doc.addObject('Part::Cut','Cut')
doc.Cut.Base = doc.brick55
doc.Cut.Tool = doc.hole33
brick55.ViewObject.hide()
hole33.ViewObject.hide()
doc.recompute()

__objs__ = []
__objs__.append(doc.getObject('Cut'))
Mesh.export(__objs__,u"/home/paul/FreeCAD models/Lego brick generated-Cut1.stl")

FreeCADGui.ActiveDocument.ActiveView.fitAll()
