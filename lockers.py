"""
lockers.py -- Paul Cobbaut, 2024-01-27
Create keychains for lockers used by blind people
"""

# Dimensions
disc_radius_mm = 21
disc_height_mm = 2
hole_radius_mm = 2

# Numbers
lockers = 10 # the number of lockers
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
def make_half_template():
    # halves start as a cylinder
    cyl = doc.addObject("Part::Cylinder", "cyl")
    cyl.Radius = disc_radius_mm
    cyl.Height = disc_height_mm/2
    # fillet the top edge
    disc = doc.addObject("Part::Fillet","disc")
    disc.Base = cyl
    edges = []
    edges.append((3,0.99,0.99))
    disc.Edges = edges
    # the hole is a cylinder
    hole = doc.addObject("Part::Cylinder", "hole")
    hole.Radius = hole_radius_mm
    hole.Height = disc_height_mm/2
    hole.Placement = FreeCAD.Placement(Vector(0, 3*(disc_radius_mm/4), 0), FreeCAD.Rotation(0,0,0), Vector(0,0,0))
    # cut the hole from the disc
    half_template = doc.addObject('Part::Cut', "half_template")
    half_template.Base = disc
    half_template.Tool = hole
    # clean up
    hole.ViewObject.hide()
    cyl.ViewObject.hide()
    disc.ViewObject.hide()
    doc.recompute()
    return half_template


def create_halves():
    # copy the half template for each locker, twice (both halves)
    for i in range(int(lockers)):
        for j in range(2):
            half = doc.addObject('Part::Feature','half')
            half.Shape = doc.half_template.Shape
            half.Label = "half_" + str(i) + '_' + str(j)
            xpos = (i+1) * separation_mm
            ypos = (j+1) * separation_mm
            half.Placement = FreeCAD.Placement(Vector(xpos, ypos, 0), FreeCAD.Rotation(0,0,0), Vector(0,0,0))
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
    # create a shapestring
    newstring=Draft.make_shapestring(String="1", FontFile=font_file, Size=7.0, Tracking=0.0)
    plm=FreeCAD.Placement() 
    plm.Base=FreeCAD.Vector(0, 0, 0)
    plm.Rotation.Q=(0, 0, 0, 1)
    newstring.Placement=plm
    newstring.Support=None
    Draft.autogroup(newstring)
    return

"""
    # pad the shapestring
    emboss = doc.addObject('Part::Extrusion','emboss')
    f = doc.getObject('emboss')
    f.Base = newstring
    f.DirMode = "Normal"
    f.DirLink = None
    f.LengthFwd = 0
    f.LengthRev = 0.30
    f.Solid = False
    f.Reversed = False
    f.Symmetric = False
    f.TaperAngle = 0
    f.TaperAngleRev = 0
    doc.recompute()
    emboss.ViewObject.hide()
    return emboss
"""

#########
# Start #
#########

# create a FreeCAD document and Part Design body
doc                 = FreeCAD.newDocument("Blindenlockers generated")
#body                = doc.addObject("PartDesign::Body", "Body")
half_template  = make_half_template()
create_halves()
create_strings()

# show in GUI
doc.recompute()
FreeCADGui.ActiveDocument.ActiveView.fitAll()
