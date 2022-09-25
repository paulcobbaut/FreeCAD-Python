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
    prism = make_prism("prism", width, length, brick_height)
    compound_list.append(prism)
    studs = create_studs("studs", compound_list, xstuds, ystuds, brick_height)
    obj = doc.addObject("Part::Compound", brickname)
    obj.Links = compound_list
    obj.Placement = FreeCAD.Placement(Vector((brick_width * offset), 0, 0), FreeCAD.Rotation(0,0,0), Vector(0,0,0))
    return obj

def tmp_create_a_brick(brickname, xstuds, ystuds, offset):
    # first create the block without studs
    # outer_prism = the brick block completely full
    # inner_prism = the part that is substracted from outer_prism, thus prism has thin walls and ceiling
    width = calculate_width(xstuds)
    length = calculate_width(ystuds)
    outer_prism = make_prism("outer_prism", width, length, brick_height)
    inner_prism = make_prism("inner_prism", width - (brick_wall * 2), length - (brick_wall * 2) , brick_height - brick_wall)
    #outer_prism.Placement = FreeCAD.Placement(Vector((brick_width * offset), 0, 0), FreeCAD.Rotation(0,0,0), Vector(0,0,0))
    inner_prism.Placement = FreeCAD.Placement(Vector(0 + brick_wall, 0 + brick_wall, 0), FreeCAD.Rotation(0,0,0), Vector(0,0,0))
    prism = doc.addObject('Part::Cut', "prism")
    prism.Base = outer_prism
    prism.Tool = inner_prism
    outer_prism.ViewObject.hide()
    inner_prism.ViewObject.hide()
    # create compound list, the object returned is a one-piece brick
    compound_list = []
    # append the block to the compound_list
    compound_list.append(prism)
    # create the studs and append each one to the compound_list
    studs = create_studs("studs", compound_list, xstuds, ystuds, brick_height)
    # brick is finished, so create a compound object with the name of the brick
    obj = doc.addObject("Part::Compound", brickname)
    obj.Links = compound_list
    obj.Placement = FreeCAD.Placement(Vector((brick_width * offset), 0, 0), FreeCAD.Rotation(0,0,0), Vector(0,0,0))
    return obj

def create_a_hole(brickname, xstuds, ystuds, offset, studs_side):
    obj = create_a_brick(brickname, xstuds, ystuds, offset)
    obj.Label = brickname
    x = (brick_width * offset) + studs_side * (brick_width + gap)  # studs_side for correct location of hole, offset for unique x location for all bricks
    y = studs_side * (brick_width + gap)                           # studs_side for correct location of hole
    obj.Placement = FreeCAD.Placement(Vector(x, y, 0), FreeCAD.Rotation(0,0,0), Vector(0,0,0))
    return obj    

def create_brick_with_hole(brickname, studsx, studsy, offset, studs_side):
    brick = create_a_brick("brick" + str(studsx) + '_' + str(studsy), studsx, studsy, offset)
    hole = create_a_hole("hole_in" + str(studsx) + '_' + str(studsy), studsx - 2 * studs_side, studsy - 2 * studs_side, offset, studs_side)
    obj = doc.addObject('Part::Cut', brickname)
    obj.Base = brick
    obj.Tool = hole
    brick.ViewObject.hide()
    hole.ViewObject.hide()
    return obj

def create_brick_series_with_hole(studs_x, studs_y_max, studs_side):
    offset = 0
    for i in range(int(studs_x), int(studs_y_max) + 1):
        brick_name = "brick_with_hole_" + str(studs_x) + 'x' + str(i) + '_border_' + str(studs_side)
        brick = create_brick_with_hole(brick_name, studs_x, i, offset, studs_side)
        offset = offset + int(studs_x) + 1
        doc.recompute()
        export = []
        export.append(doc.getObject(brick_name))
        Mesh.export(export, u"/home/paul/FreeCAD models/brick_python/" + brick_name + ".stl")

tmp_create_a_brick("brick_2x4", 2, 4, 0)
tmp_create_a_brick("brick_2x4", 2, 6, 3)
tmp_create_a_brick("brick_2x4", 2, 8, 6)
doc.recompute()

# create_brick_series_with_hole (studs X, studs Y, side thickness in studs)
#
# minimal xstuds = 3!!!
# studs_y is always greater than or equal to studs_x!!!
# --> because bricks are always named shortest_side x longest_side
# --> for example 5x3 does not exist, it is 3x5
# minimal X studs = 3!!!
# --> cannot have a hole in a 2x2, 2x3 or 3x2 brick
##create_brick_series_with_hole(3, 8, 1)
##create_brick_series_with_hole(6, 10, 2)

FreeCADGui.ActiveDocument.ActiveView.fitAll()
