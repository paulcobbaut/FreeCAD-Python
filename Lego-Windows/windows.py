#!/usr/bin/python
#windows.py -- Paul Cobbaut, 2024-08-19

import FreeCAD
from FreeCAD import Base, Vector
import Part
import Sketcher
import Mesh
import MeshPart

# Labels
DocLabel  = 'Lego_Windows'
BodyLabel = DocLabel + '_body'
HullLabel = DocLabel + '_hull'
StudLabel = 'stud_template'
xLabel   = DocLabel + '_x'
xLabel   = DocLabel + '_x'

# The directory to export the .stl files to
export_directory = "/home/paul/FreeCAD_generated/windows/"

# Dimensions for studs
stud_oradius_mm		= 2.450		# Lego official is 2.400
stud_iradius_mm		= 1.400		
stud_center_spacing_mm	= 8.000
stud_height_mm		= 1.700		# Lego official is 1.600

# Dimensions for plates
plate_height_mm		= 3.200
plate_width_mm		= 7.800

# The gap that is added to the width/length for each extra stud
gap_mm 			= 0.200

# Dimensions for bricks
brick_height_mm		= 9.600		# plate_height_mm * 3
brick_width_mm		= 7.800		# = plate_width_mm

# Side thickness for windows
side_mm	        = 1.450	

def make_3mf(name, compound):
    cobj = doc.addObject("Part::Compound", name)
    cobj.Links = compound
    doc.recompute()
    export_list = []
    export_list.append(cobj)
    Mesh.export(export_list, u"/home/paul/FreeCAD_generated/" + name + ".stl")

# create a standard x, y, z box in FreeCAD
def make_box(name, x, y, z):
    obj = doc.addObject("Part::Box", name)
    obj.Length = x
    obj.Width  = y
    obj.Height = z
    return obj

# convert studs to mm for bricks and plates
# one stud on brick	= 1 * brick_width_mm
# two studs on brick	= 2 * brick_width_mm + 1 * gap_mm
# three studs on brick	= 3 * brick_width_mm + 2 * gap_mm
# plate_width_mm is identical to brick_width_mm
def convert_studs_to_mm(studs):
    mm = (studs * brick_width_mm) + ((studs - 1) * gap_mm)
    return mm

# the stud template is created once then always copied
def make_stud(name):
    o_cyl = doc.addObject("Part::Cylinder", "o_cyl")
    o_cyl.Radius = stud_oradius_mm
    o_cyl.Height = stud_height_mm
    i_cyl = doc.addObject("Part::Cylinder", "i_cyl")
    i_cyl.Radius = stud_iradius_mm
    i_cyl.Height = stud_height_mm
    stud  = doc.addObject('Part::Cut', name)
    stud.Base = o_cyl
    stud.Tool = i_cyl
    doc.recompute()
    return stud

# START
doc = FreeCAD.newDocument(DocLabel)       # create document
stud_template = make_stud(StudLabel)      # create stud template
stud_template.ViewObject.hide()           # hide stud template

# make window hull
owidth  = convert_studs_to_mm(2)
odepth  = brick_width_mm
oheight = brick_height_mm * 2
outer  = make_box("outer", owidth, odepth, oheight)
iwidth  = convert_studs_to_mm(2) - (side_mm * 2)
idepth  = brick_width_mm
iheight = (brick_height_mm * 2) - (side_mm * 2)
inner  = make_box("inner", iwidth, idepth, iheight)
inner.Placement = FreeCAD.Placement(Vector(side_mm, 0, side_mm), FreeCAD.Rotation(0,0,0), Vector(0,0,0))
hull   = doc.addObject('Part::Cut', HullLabel)
hull.Base = outer
hull.Tool = inner
doc.recompute()
outer.ViewObject.hide()
inner.ViewObject.hide()


# add studs on window
stud1 = doc.addObject('Part::Feature',StudLabel)
stud1.Shape = doc.stud_template.Shape 
stud1.Label = "stud1"
xpos = (stud_center_spacing_mm) - (stud_center_spacing_mm / 2) - (gap_mm / 2)
ypos = (stud_center_spacing_mm) - (stud_center_spacing_mm / 2) - (gap_mm / 2)
zpos = oheight
stud1.Placement = FreeCAD.Placement(Vector(xpos, ypos, zpos), FreeCAD.Rotation(0,0,0), Vector(0,0,0))
doc.recompute()

stud2 = doc.addObject('Part::Feature',StudLabel)
stud2.Shape = doc.stud_template.Shape 
stud2.Label = "stud2"
xpos = (2 * stud_center_spacing_mm) - (stud_center_spacing_mm / 2) - (gap_mm / 2)
ypos = (stud_center_spacing_mm) - (stud_center_spacing_mm / 2) - (gap_mm / 2)
zpos = oheight
stud2.Placement = FreeCAD.Placement(Vector(xpos, ypos, zpos), FreeCAD.Rotation(0,0,0), Vector(0,0,0))
doc.recompute()


# add bottom holes
# each hole is a cylinder at the stud location, followed by y-axis straight hole
# cylinder holes
hole1 = doc.addObject("Part::Cylinder", "hole1")
hole1.Radius = stud_oradius_mm 
hole1.Height = stud_height_mm
xpos = (stud_center_spacing_mm) - (stud_center_spacing_mm / 2) - (gap_mm / 2)
ypos = (stud_center_spacing_mm) - (stud_center_spacing_mm / 2) - (gap_mm / 2)
zpos = 0
hole1.Placement = FreeCAD.Placement(Vector(xpos, ypos, zpos), FreeCAD.Rotation(0,0,0), Vector(0,0,0))
doc.recompute()

onehole      = doc.addObject('Part::Cut', "onehole")
onehole.Base = hull
onehole.Tool = hole1

hole2 = doc.addObject("Part::Cylinder", "hole2")
hole2.Radius = stud_oradius_mm 
hole2.Height = stud_height_mm
xpos = (2 * stud_center_spacing_mm) - (stud_center_spacing_mm / 2) - (gap_mm / 2)
ypos = (stud_center_spacing_mm) - (stud_center_spacing_mm / 2) - (gap_mm / 2)
zpos = 0
hole2.Placement = FreeCAD.Placement(Vector(xpos, ypos, zpos), FreeCAD.Rotation(0,0,0), Vector(0,0,0))
doc.recompute()

twohole      = doc.addObject('Part::Cut', "twohole")
twohole.Base = onehole
twohole.Tool = hole2

# follow-up straight holes
h1width  = stud_oradius_mm * 2
h1depth  = stud_oradius_mm * 2
h1height = side_mm
h1       = make_box("h1", h1width, h1depth, h1height)
xpos = (stud_center_spacing_mm) - (stud_center_spacing_mm / 2) - (gap_mm / 2) - (stud_oradius_mm) 
ypos = (stud_center_spacing_mm) - (stud_center_spacing_mm / 2) - (gap_mm / 2)
zpos = 0
h1.Placement = FreeCAD.Placement(Vector(xpos, ypos, zpos), FreeCAD.Rotation(0,0,0), Vector(0,0,0))
doc.recompute()

threehole      = doc.addObject('Part::Cut', "threehole")
threehole.Base = twohole
threehole.Tool = h1

h2width  = stud_oradius_mm * 2
h2depth  = stud_oradius_mm * 2
h2height = side_mm
h2       = make_box("h2", h2width, h2depth, h2height)
xpos = (2 * stud_center_spacing_mm) - (stud_center_spacing_mm / 2) - (gap_mm / 2) - (stud_oradius_mm) 
ypos = (stud_center_spacing_mm) - (stud_center_spacing_mm / 2) - (gap_mm / 2)
zpos = 0
h2.Placement = FreeCAD.Placement(Vector(xpos, ypos, zpos), FreeCAD.Rotation(0,0,0), Vector(0,0,0))
doc.recompute()

fourhole      = doc.addObject('Part::Cut', "fourhole")
fourhole.Base = threehole
fourhole.Tool = h2

# fusion the studs
fuse1 = doc.addObject("Part::Fuse","fuse1")
fuse1.Base = fourhole
fuse1.Tool = stud1
fuse2 = doc.addObject("Part::Fuse","fuse2")
fuse2.Base = fuse1
fuse2.Tool = stud2

# add window frames similar to the windows of my grandmothers house
uwidth  = side_mm
udepth  = side_mm
uheight = convert_studs_to_mm(2) - (side_mm * 3) 
upwards  = make_box("upwards", uwidth, udepth, uheight)
upwards.Placement = FreeCAD.Placement(Vector(brick_width_mm - (side_mm / 2), 0, side_mm), FreeCAD.Rotation(0,0,0), Vector(0,0,0))

fwidth  = convert_studs_to_mm(2) - (side_mm * 2)
fdepth  = side_mm
fheight = side_mm
flat  = make_box("flat", fwidth, fdepth, fheight)
flat.Placement = FreeCAD.Placement(Vector(side_mm, 0, uheight + side_mm), FreeCAD.Rotation(0,0,0), Vector(0,0,0))



doc.removeObject("stud_template")
doc.removeObject("o_cyl")
doc.removeObject("i_cyl")

doc.recompute()
FreeCADGui.ActiveDocument.ActiveView.fitAll()

