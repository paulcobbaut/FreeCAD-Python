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

def create_studs(name, compound_list, x, y, z):
    for i in range(int(x)):
        for j in range(int(y)):
            obj = doc.addObject('Part::Feature','stud_template')
            obj.Shape = doc.stud_template.Shape
            obj.Label = name + str(i) + '__' + str(j)
            xpos = ((i+1) * stud_center_spacing) - (stud_center_spacing / 2)
            ypos = ((j+1) * stud_center_spacing) - (stud_center_spacing / 2)
            obj.Placement = FreeCAD.Placement(Vector(xpos, ypos, z), FreeCAD.Rotation(0,0,0), Vector(0,0,0))
            compound_list.append(obj)

def create_a_brick(brickname, xstuds, ystuds, offset):
    compound_list = []
    width = calculate_width(xstuds)
    length = calculate_width(ystuds)
    prism = make_prism("prism", width, length, plate_height)
    compound_list.append(prism)
    studs = create_studs("studs", compound_list, xstuds, ystuds, plate_height)
    obj = doc.addObject("Part::Compound", brickname)
    obj.Links = compound_list
    obj.Placement = FreeCAD.Placement(Vector((brick_width * offset), 0, 0), FreeCAD.Rotation(0,0,0), Vector(0,0,0))
    return obj

def create_a_hole(brickname, xstuds, ystuds, offset):
    obj = create_a_brick(brickname, xstuds, ystuds, offset)
    obj.Label = brickname
    obj.Placement = FreeCAD.Placement(Vector((brick_width * offset) + brick_width + gap, brick_width + gap, 0), FreeCAD.Rotation(0,0,0), Vector(0,0,0))
    return obj    

def create_brick_with_hole(brickname, studsx, studsy, offset):
    brick = create_a_brick("brick" + str(studsx) + '_' + str(studsy), studsx, studsy, offset)
    hole = create_a_hole("hole" + str(studsx) + '_' + str(studsy), studsx - 2, studsy - 2, offset)
    obj = doc.addObject('Part::Cut', brickname)
    obj.Base = brick
    obj.Tool = hole
    brick.ViewObject.hide()
    hole.ViewObject.hide()
    return obj

def create_brick_series_with_hole(studsx, studsymax):
    offset = 0
    for i in range(int(studsx), int(studsymax) + 1):
        brickname = "brick" + str(studsx) + 'x' + str(i)
        brick = create_brick_with_hole(brickname, studsx, i, offset)
        offset = offset + int(studsx) + 1
        doc.recompute()
        export = []
        export.append(doc.getObject(brickname))
        Mesh.export(export, u"/home/paul/FreeCAD models/brick_python/" + brickname + ".stl")

# minimal xstuds = 3!
create_brick_series_with_hole(3,12)
create_brick_series_with_hole(4,12)
create_brick_series_with_hole(5,12)
FreeCADGui.ActiveDocument.ActiveView.fitAll()
