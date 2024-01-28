"""
lockers.py -- Paul Cobbaut, 2024-01-27
Create keychains for lockers used by blind people
"""

# Dimensions
disc_radius_mm = 21
disc_height_mm = 2
hole_radius_mm = 2

# Numbers
lockers = 23 # the number of lockers
separation_mm = 50 # mm_between_centers_in_FreeCAD_GUI

# The directory to export the .stl files to
export_directory = "/home/paul/FreeCAD_generated/lockers/"

# font 
font_file="/usr/share/fonts/truetype/freefont/FreeSans.ttf" 

import FreeCAD
from FreeCAD import Base, Vector
import Part
import PartDesign
import Sketcher
import Mesh
import MeshPart
import Draft
import math


# keychain is printed in two halves
# top has braille number extruded on it
# bottom has number and "markgrave" extruded on it
def make_tophalf_template():
    # get the half disc
    tophalf = make_half_disc("tophalf")
    # extrude text MARKGRAVE
    MARKGRAVE = create_wmstring("MARKGRAVE")
    xpos = -13  # hardcoded...
    ypos = -13
    zpos = disc_height_mm/2
    MARKGRAVE.Placement = FreeCAD.Placement(Vector(xpos, ypos, zpos), FreeCAD.Rotation(0,0,0), Vector(0,0,0))
    # extrude text VZW
    VZW       = create_wmstring("VZW")
    xpos = 1 - disc_radius_mm/4
    ypos = 3 - disc_radius_mm
    zpos = disc_height_mm/2
    VZW.Placement = FreeCAD.Placement(Vector(xpos, ypos, zpos), FreeCAD.Rotation(0,0,0), Vector(0,0,0))
    # create compound of the half disc and the extruded texts
    compound_list = []
    compound_list.append(tophalf)
    compound_list.append(MARKGRAVE)
    compound_list.append(VZW)
    tophalf_template = doc.addObject("Part::Compound", "tophalf_template")
    tophalf_template.Links = compound_list
    # cleanup
    tophalf.ViewObject.hide()
    MARKGRAVE.ViewObject.hide()
    VZW.ViewObject.hide()
    return tophalf_template

def make_bothalf_template():
    bothalf_template = make_half_disc("bothalf_template")
    xpos = 0
    ypos = - separation_mm
    zpos = disc_height_mm/2
    bothalf_template.Placement = FreeCAD.Placement(Vector(xpos, ypos, zpos), FreeCAD.Rotation(0,0,0), Vector(0,0,0))
    return bothalf_template

def make_half_disc(name):
    # halves start as a cylinder
    cyl = doc.addObject("Part::Cylinder", name + "_cyl")
    cyl.Radius = disc_radius_mm
    cyl.Height = disc_height_mm/2
    # fillet the top edge
    disc = doc.addObject("Part::Fillet",name + "_disc")
    disc.Base = cyl
    edges = []
    edges.append((3,0.99,0.99))
    disc.Edges = edges
    # the hole is a cylinder
    hole = doc.addObject("Part::Cylinder", name + "_hole")
    hole.Radius = hole_radius_mm
    hole.Height = disc_height_mm/2
    hole.Placement = FreeCAD.Placement(Vector(0, 3*(disc_radius_mm/4), 0), FreeCAD.Rotation(0,0,0), Vector(0,0,0))
    # cut the hole from the disc
    half_template = doc.addObject('Part::Cut', name)
    f = doc.getObject(name)
    f.Base = disc
    f.Tool = hole
    f.Label = name
    # clean up
    hole.ViewObject.hide()
    cyl.ViewObject.hide()
    disc.ViewObject.hide()
    doc.recompute()
    return f


def create_wmstring(text):
    # hardcoded value
    font_size = 1.5
    # create string containing watermark
    wmstring=Draft.make_shapestring(String=text, FontFile=font_file, Size=font_size, Tracking=0.0)
    #xpos = 0
    #ypos = 0
    #zpos = disc_height_mm/2
    #wmstring.Placement = FreeCAD.Placement(Vector(xpos, ypos, zpos), FreeCAD.Rotation(0,0,0), Vector(0,0,0))
    wmstring.Support=None
    wmstring.Label=text + '_string'
    Draft.autogroup(wmstring)
    # extrude the shapestring
    emboss = doc.addObject('Part::Extrusion',text + '_emboss')
    f = doc.getObject(text + '_emboss')
    f.Base = wmstring
    f.DirMode = "Normal"
    f.DirLink = None
    f.LengthFwd = 0.50
    f.LengthRev = 0
    f.Solid = False
    f.Reversed = False
    f.Symmetric = False
    f.TaperAngle = 0
    f.TaperAngleRev = 0
    f.Label=text
    doc.recompute()
    wmstring.ViewObject.hide()
    return f


def create_halves():
    # hardcoded values for the numbers on tophalf
    font_size = 10
    font_offset = 7
    # copy the half template for each locker, twice (both halves)
    for i in range(int(lockers)):
        # copy tophalf template
        tophalf = doc.addObject('Part::Feature','tophalf')
        tophalf.Shape = doc.tophalf_template.Shape
        tophalf.Label = "tophalf_" + str(i+1) 
        # position tophalf copy in FreeCAD GUI
        xpos = (i+1) * separation_mm
        ypos = separation_mm
        tophalf.Placement = FreeCAD.Placement(Vector(xpos, ypos, 0), FreeCAD.Rotation(0,0,0), Vector(0,0,0))
        # create a shapestring
        sname = 'string_' + str(i+1)              # name of the shapestring
        ename = 'string_' + str(i+1) + '_extrude' # name of the extrude
        newstring=Draft.make_shapestring(String=str(i+1), FontFile=font_file, Size=font_size, Tracking=0.0)
        # position the shapestring (shift double digit numbers to the left)
        if (i<9):
            xpos = (i+1) * separation_mm
        else:
            xpos = (i+1) * separation_mm - 15
        ypos = separation_mm - font_offset
        zpos = disc_height_mm/2
        newstring.Placement = FreeCAD.Placement(Vector(xpos, ypos, zpos), FreeCAD.Rotation(0,0,0), Vector(0,0,0))
        newstring.Support = None
        newstring.Label = sname
        Draft.autogroup(newstring)
        # extrude the shapestring
        newextrude = doc.addObject('Part::Extrusion',ename)
        f = doc.getObject(ename)
        f.Base = newstring
        f.DirMode = "Normal"
        f.DirLink = None
        f.LengthFwd = 1
        f.LengthRev = 0
        f.Solid = False
        f.Reversed = False
        f.Symmetric = False
        f.TaperAngle = 0
        f.TaperAngleRev = 0
        f.Label = ename
        # compund extrusion with tophalf
        tmp_compound = []
        tmp_compound.append(tophalf)
        tmp_compound.append(f)
        obj = doc.addObject("Part::Compound", 'compound_' + str(i+1))
        obj.Links = tmp_compound
        obj.Label = 'compound_' + str(i+1)

        # copy bottomhalf template
        bothalf = doc.addObject('Part::Feature','bothalf')
        bothalf.Shape = doc.bothalf_template.Shape
        bothalf.Label = "bothalf_" + str(i+1) 
        # position bottomhalf copy in FreeCAD GUI
        xpos = (i+1) * separation_mm
        ypos = - separation_mm
        bothalf.Placement = FreeCAD.Placement(Vector(xpos, ypos, 0), FreeCAD.Rotation(0,0,0), Vector(0,0,0))
    return


#########
# Start #
#########

# create a FreeCAD document 
doc               = FreeCAD.newDocument("Blindenlockers generated")
tophalf_template  = make_tophalf_template()
bothalf_template  = make_bothalf_template()
create_halves()

##doc.removeObject("loft")
# show in GUI
doc.recompute()
FreeCADGui.ActiveDocument.ActiveView.fitAll()
