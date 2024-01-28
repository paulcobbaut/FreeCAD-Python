"""
lockers.py -- Paul Cobbaut, 2024-01-27
Create keychains for lockers used by blind people
"""

# Dimensions
disc_radius_mm = 21
disc_height_mm = 2
hole_radius_mm = 2

# Numbers
lockers = 12 # the number of lockers
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
    # pad the shapestring
    emboss = doc.addObject('Part::Extrusion',text + '_emboss')
    f = doc.getObject(text + '_emboss')
    f.Base = wmstring
    f.DirMode = "Normal"
    f.DirLink = None
    f.LengthFwd = 0.40
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
    # copy the half template for each locker, twice (both halves)
    for i in range(int(lockers)):
        tophalf = doc.addObject('Part::Feature','tophalf')
        tophalf.Shape = doc.tophalf_template.Shape
        tophalf.Label = "tophalf_" + str(i+1) 
        xpos = (i+1) * separation_mm
        ypos = separation_mm
        tophalf.Placement = FreeCAD.Placement(Vector(xpos, ypos, 0), FreeCAD.Rotation(0,0,0), Vector(0,0,0))
        bothalf = doc.addObject('Part::Feature','bothalf')
        bothalf.Shape = doc.bothalf_template.Shape
        bothalf.Label = "bothalf_" + str(i+1) 
        xpos = (i+1) * separation_mm
        ypos = - separation_mm
        bothalf.Placement = FreeCAD.Placement(Vector(xpos, ypos, 0), FreeCAD.Rotation(0,0,0), Vector(0,0,0))
    return

"""
def create_mesh_and_export(string_text, compound_list):
    obj = doc.addObject("Part::Compound", "CompoundAll")
    obj.Links = compound_list
    doc.recompute()
    # emboss the text
    embossed = doc.addObject('Part::Cut', "embossed")
    embossed.Base = obj
    embossed.Tool = emboss
    doc.recompute()
    # create mesh from shape (compound)
    mesh = doc.addObject("Mesh::Feature","Mesh-" + string_text)
    part = doc.getObject("embossed")
    shape = Part.getShape(part,"")
    mesh.Mesh = MeshPart.meshFromShape(Shape=shape, LinearDeflection=1, AngularDeflection=0.1, Relative=False)
    mesh.Label = 'Mesh-' + string_text
    # upload .stl file
    export = []
    export.append(mesh)
    Mesh.export(export, export_directory + string_text + ".stl")
    #return obj
"""


def create_strings():
    # hardcoded values...
    font_size = 8
    font_offset = 10
    # create a shapestring
    for i in range(int(lockers)):
        newstring=Draft.make_shapestring(String=str(i+1), FontFile=font_file, Size=font_size, Tracking=0.0)
        xpos = (i+1) * separation_mm
        ypos = separation_mm - font_offset
        zpos = disc_height_mm/2
        newstring.Placement = FreeCAD.Placement(Vector(xpos, ypos, zpos), FreeCAD.Rotation(0,0,0), Vector(0,0,0))
        newstring.Support=None
        Draft.autogroup(newstring)
    return


#########
# Start #
#########

# create a FreeCAD document and Part Design body
doc                 = FreeCAD.newDocument("Blindenlockers generated")
#body                = doc.addObject("PartDesign::Body", "Body")
tophalf_template  = make_tophalf_template()
bothalf_template  = make_bothalf_template()
create_halves()
create_strings()

##doc.removeObject("loft")
# show in GUI
doc.recompute()
FreeCADGui.ActiveDocument.ActiveView.fitAll()
