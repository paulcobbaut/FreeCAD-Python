#!/usr/bin/python
#windows.py -- Paul Cobbaut, 2024-08-19

import FreeCAD
from FreeCAD import Base, Vector, Placement
import Part
import Sketcher
import Mesh
import MeshPart

# Labels
DocLabel   = 'Lego_Windows'
BodyLabel  = DocLabel + '_body'
HullLabel  = DocLabel + '_hull'  # hull = outer (wood) edge of window
FrameLabel = DocLabel + '_frame' # frame = inner (wood) beams in window
StudsLabel = DocLabel + '_studs' # studs on top
HolesLabel = DocLabel + '_hole'  # hole = disc + prism
DiscsLabel = DocLabel + '_disc'
PrismLabel = DocLabel + '_prism'
StudLabel  = 'stud_template'    # a single template stud

# The directory to export the .stl files to
export_directory = "/home/paul/FreeCAD_generated/windows/"

# Dimensions
stud_oradius_mm	= 2.450		# Lego official is 2.400
stud_iradius_mm	= 1.400		
stud_spacing_mm	= 8.000
stud_height_mm	= 1.700		# Lego official is 1.600
brick_height_mm	= 9.600
brick_width_mm	= 7.800
gap_mm 			= 0.200     # gap per extra stud
side_mm	        = 1.450     # side thickness for windows

# create a standard x, y, z box in FreeCAD
def make_box(name, x, y, z):
    obj = doc.addObject("Part::Box", name)
    obj.Length = x
    obj.Width  = y
    obj.Height = z
    return obj

# convert studs to mm for bricks and plates
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

# the edge of the window
def make_window_hull(name, width_in_studs, height_in_bricks):
    owidth  = convert_studs_to_mm(width_in_studs)
    odepth  = brick_width_mm
    oheight = brick_height_mm * height_in_bricks
    outer   = make_box("outer", owidth, odepth, oheight)
    iwidth  = convert_studs_to_mm(width_in_studs) - (side_mm * 2)
    idepth  = brick_width_mm
    iheight = (brick_height_mm * height_in_bricks) - (side_mm * 2)
    inner  = make_box("inner", iwidth, idepth, iheight)
    inner.Placement = Placement(Vector(side_mm, 0, side_mm), FreeCAD.Rotation(0,0,0), Vector(0,0,0))
    hull   = doc.addObject('Part::Cut', name)
    hull.Base = outer
    hull.Tool = inner
    doc.recompute()
    outer.ViewObject.hide()
    inner.ViewObject.hide()
    return hull

# add window frames similar to the windows of my grandmothers house
def make_grandmother_frame(name, width_in_studs, height_in_bricks):
    uwidth  = side_mm
    udepth  = side_mm
    uheight = convert_studs_to_mm(height_in_bricks) - (side_mm * 3) 
    upwards = make_box("upwards", uwidth, udepth, uheight)
    upwards.Placement = Placement(Vector( ((width_in_studs * brick_width_mm)/2) - (side_mm / 2), 0, side_mm), FreeCAD.Rotation(0,0,0), Vector(0,0,0))
    fwidth  = convert_studs_to_mm(width_in_studs) - (side_mm * 2)
    fdepth  = side_mm
    fheight = side_mm
    flat    = make_box("flat", fwidth, fdepth, fheight)
    flat.Placement = Placement(Vector(side_mm, 0, uheight + side_mm), FreeCAD.Rotation(0,0,0), Vector(0,0,0))
    obj = doc.addObject("Part::Fuse",name)
    obj.Base = upwards
    obj.Tool = flat
    return obj 

def add_studs(name, width_in_studs, height_in_bricks):
    studlist = []
    for i in range(int(width_in_studs)):
        label = name + '_' + str(i + 1)
        stud = doc.addObject('Part::Feature',label)
        stud.Shape = doc.stud_template.Shape 
        stud.Label = label
        x = ((i+1) * stud_spacing_mm) - (stud_spacing_mm / 2) - (gap_mm / 2)
        y = (stud_spacing_mm) - (stud_spacing_mm / 2) - (gap_mm / 2)
        z = brick_height_mm * height_in_bricks
        stud.Placement = Placement(Vector(x, y, z), FreeCAD.Rotation(0,0,0), Vector(0,0,0))
        studlist.append(stud)
        doc.recompute()
    obj = doc.addObject("Part::MultiFuse",name)
    obj.Shapes = studlist
    obj.Label = name
    doc.recompute()
    return obj

def add_holes(name, width_in_studs, height_in_bricks):
    holelist = []
    for i in range(int(width_in_studs)):
        # stud shaped hole
        label = DiscsLabel + '_' + str(i + 1)
        disc  = doc.addObject("Part::Cylinder", label)
        disc.Radius = stud_oradius_mm 
        disc.Height = side_mm
        x = ((i+1) * stud_spacing_mm) - (stud_spacing_mm / 2) - (gap_mm / 2)
        y = (stud_spacing_mm) - (stud_spacing_mm / 2) - (gap_mm / 2)
        z = 0
        disc.Placement = Placement(Vector(x, y, z), FreeCAD.Rotation(0,0,0), Vector(0,0,0))
        # follow-up straight hole
        label  = PrismLabel + '_' + str(i + 1)
        edge   = stud_oradius_mm * 2
        prism  = make_box(label, edge, edge, side_mm)
        x = ((i+1) * stud_spacing_mm) - (stud_spacing_mm / 2) - (gap_mm / 2) - (stud_oradius_mm) 
        y = (stud_spacing_mm) - (stud_spacing_mm / 2) - (gap_mm / 2)
        z = 0
        prism.Placement = Placement(Vector(x, y, z), FreeCAD.Rotation(0,0,0), Vector(0,0,0))
        doc.recompute()
        label  = HolesLabel + '_' + str(i + 1)
        hole      = doc.addObject('Part::Fuse', label)
        hole.Base = disc
        hole.Tool = prism
        holelist.append(hole)
    obj = doc.addObject("Part::MultiFuse",name)
    obj.Shapes = holelist
    obj.Label = name
    doc.recompute()
    return obj



# START
doc = FreeCAD.newDocument(DocLabel)       # create document
stud_template = make_stud(StudLabel)      # create stud template

w = 5 # width in studs of the window
h = 2 # height in bricks 

hull  = make_window_hull(HullLabel, w, h)
frame = make_grandmother_frame(FrameLabel, w, h)
studs = add_studs(StudsLabel, w, h)
holes = add_holes(HolesLabel, w, h)

obj = doc.addObject("Part::MultiFuse","obj")
obj.Shapes = [hull, frame, studs]
obj.Label = "obj"
doc.recompute()
window   = doc.addObject('Part::Cut', "window")
window.Base = obj
window.Tool = holes
doc.recompute()

doc.removeObject("stud_template")
doc.removeObject("i_cyl")
doc.removeObject("o_cyl")
doc.recompute()
FreeCADGui.ActiveDocument.ActiveView.fitAll()
