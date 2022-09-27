"""
brick_FreeCAD.py -- Paul Cobbaut, 2022-09-25
The goal is to make nonexisting Lego-compatible pieces for use in 3D printer
The script is able to generate .stl files directly.
"""
# Dimensions for studs
stud_radius_mm		= 2.471
stud_center_spacing_mm	= 8.000
stud_height_mm		= 1.700

# Dimensions for plates
plate_height_mm		= 3.200
plate_width_mm		= 7.800		# for 1x1 plate and 1x1 brick

# The gap that is added to the width/lenght for each extra stud
gap_mm 			= 0.200		# extra thickness needed between each two studs

# Dimensions for bricks
brick_height_mm		= 9.600		# plate_height_mm * 3
brick_wall_thickness_mm	= 1.600	
brick_width_mm		= 7.800		# = plate_width_mm

# Dimensions for bricks: underside standard Lego-compatible brick
cylinder_radius_outer_mm = 3.226	# 3.256?
cylinder_radius_inner_mm = 2.370	# 2.400?
cylinder_height_mm 	= 8.000

import FreeCAD
from FreeCAD import Base, Vector
import Part
import Sketcher
import Mesh

# FreeCAD document
doc = FreeCAD.newDocument("Lego brick generated")
obj = doc.addObject("PartDesign::Body", "Body")

def calculate_width(y):
    w = (y * (brick_width_mm + gap_mm)) - gap_mm
    return w

def make_prism(name, x, y, z):
    obj = doc.addObject("Part::Box", name)
    obj.Length = x
    obj.Width = y
    obj.Height = z
    doc.recompute()
    return obj

# the stud template is always copied
def make_stud(name):
    obj = doc.addObject("Part::Cylinder", name)
    obj.Radius = stud_radius_mm
    obj.Height = stud_height_mm
    doc.recompute()
    return obj

stud_template = make_stud("stud_template")
stud_template.ViewObject.hide()

# the cylinder template is always copied
def make_cylinder(name):
    outer_cylinder = doc.addObject("Part::Cylinder", "outer_cylinder")
    outer_cylinder.Radius = cylinder_radius_outer_mm
    outer_cylinder.Height = cylinder_height_mm
    inner_cylinder = doc.addObject("Part::Cylinder", "inner_cylinder")
    inner_cylinder.Radius = cylinder_radius_inner_mm
    inner_cylinder.Height = cylinder_height_mm
    cylinder = doc.addObject('Part::Cut', name)
    cylinder.Base = outer_cylinder
    cylinder.Tool = inner_cylinder
    outer_cylinder.ViewObject.hide()
    inner_cylinder.ViewObject.hide()
    return cylinder

cylinder_template = make_cylinder("cylinder_template")
cylinder_template.ViewObject.hide()


def create_studs(name, compound_list, x, y, z):
    for i in range(int(x)):
        for j in range(int(y)):
            obj = doc.addObject('Part::Feature','stud_template')
            obj.Shape = doc.stud_template.Shape
            obj.Label = name + str(i) + '__' + str(j)
            xpos = ((i+1) * stud_center_spacing_mm) - (stud_center_spacing_mm / 2)
            ypos = ((j+1) * stud_center_spacing_mm) - (stud_center_spacing_mm / 2)
            obj.Placement = FreeCAD.Placement(Vector(xpos, ypos, z), FreeCAD.Rotation(0,0,0), Vector(0,0,0))
            compound_list.append(obj)


def create_a_brick(brickname, xstuds, ystuds, offset):
    compound_list = []
    width = calculate_width(xstuds)
    length = calculate_width(ystuds)
    prism = make_prism("prism", width, length, brick_height_mm)
    compound_list.append(prism)
    studs = create_studs("studs", compound_list, xstuds, ystuds, brick_height_mm)
    obj = doc.addObject("Part::Compound", brickname)
    obj.Links = compound_list
    obj.Placement = FreeCAD.Placement(Vector((brick_width_mm * offset), 0, 0), FreeCAD.Rotation(0,0,0), Vector(0,0,0))
    return obj


def tmp_create_a_brick(brickname, xstuds, ystuds, offset):
    # first create the block without studs
    # outer_prism = the brick block completely full
    # inner_prism = the part that is substracted from outer_prism, thus prism has thin walls and ceiling
    width = calculate_width(xstuds)
    length = calculate_width(ystuds)
    outer_prism = make_prism("outer_prism", width, length, brick_height_mm)
    inner_prism = make_prism("inner_prism", width - (brick_wall_thickness_mm * 2), length - (brick_wall_thickness_mm * 2) , brick_height_mm - brick_wall_thickness_mm)
    inner_prism.Placement = FreeCAD.Placement(Vector(brick_wall_thickness_mm, brick_wall_thickness_mm, 0), FreeCAD.Rotation(0,0,0), Vector(0,0,0))
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
    studs = create_studs("studs", compound_list, xstuds, ystuds, brick_height_mm)
    # create the bottom cylinders
    for j in range(int(xstuds - 1)):
        for i in range(int(ystuds - 1)):
            newcyl = doc.addObject('Part::Feature','cylinder_template')
            newcyl.Shape = doc.cylinder_template.Shape
            newcyl.Label = 'cylinder_' + str(i)
            xpos = (brick_width_mm + gap_mm) * (j + 1)
            ypos = (brick_width_mm + gap_mm) * (i + 1)
            newcyl.Placement = FreeCAD.Placement(Vector(xpos, ypos, 0), FreeCAD.Rotation(0,0,0), Vector(0,0,0))
            compound_list.append(newcyl)
    # brick is finished, so create a compound object with the name of the brick
    obj = doc.addObject("Part::Compound", brickname)
    obj.Links = compound_list
    obj.Placement = FreeCAD.Placement(Vector((brick_width_mm * offset), 0, 0), FreeCAD.Rotation(0,0,0), Vector(0,0,0))
    return obj

def create_a_hole(brickname, xstuds, ystuds, offset, studs_side):
    obj = create_a_brick(brickname, xstuds, ystuds, offset)
    obj.Label = brickname
    x = (brick_width_mm * offset) + studs_side * (brick_width_mm + gap_mm)  # studs_side for correct location of hole, offset for unique x location for all bricks
    y = studs_side * (brick_width_mm + gap_mm)                           # studs_side for correct location of hole
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

#tmp_create_a_brick("brick_2x3", 2, 3, 0)
#tmp_create_a_brick("brick_2x4", 3, 4, 3)
#tmp_create_a_brick("brick_13x25", 13, 25, 0)
#tmp_create_a_brick("brick_2x6", 2, 6, 9)

# create_brick_series_with_hole (studs X, studs Y, side thickness in studs)
#
# minimal xstuds = 3!!!
# studs_y is always greater than or equal to studs_x!!!
# --> because bricks are always named shortest_side x longest_side
# --> for example 5x3 does not exist, it is 3x5
# minimal X studs = 3!!!
# --> cannot have a hole in a 2x2, 2x3 or 3x2 brick
# pot = create_brick_with_hole("pot",13, 30, 0, 1)
#create_brick_series_with_hole(3, 8, 1)
create_brick_series_with_hole(6, 12, 2)

doc.recompute()
FreeCADGui.ActiveDocument.ActiveView.fitAll()
