"""
fc1.py
Paul Cobbaut, 2022-07-02
First attempt at FreeCAD scripting
"""

import FreeCAD
from FreeCAD import Base, Vector
import Arch
import Draft
import Part
import importSVG
import BOPTools
import BOPTools.JoinFeatures


# FreeCAD document
document = FreeCAD.activeDocument()
document_name = "Scripted"

# SVG file to be imported
svg_filename = "/home/paul/drawing.svg"

# number of pieces in grid (max 25!)
rows = 2
cols = 2


# Dimensions for squared puzzle pieces in mm
""" top view showing width and length (x and y in FreeCAD)

      Width x
   ______________
  |              | L
  |              | e
  |              | n
  |              | g
  |              | t
  |              | h
  |              |
  |______________| y 


"""
piece_length = 200               # X-coordinate in FreeCAD
piece_width = piece_length       # Y-coordinate in FreeCAD
piece_height = 4                 # Z-coordinate in FreeCAD
#piece_separation = piece_length / 5
piece_separation = 0


# Names and tuples for the tenons and mortises
""" top view showing: - names for mortises on the top and the left
                      - names for tenons on the right and the bottom

           top_left   top_right
              _____________
             |  |_|   |_|  |
             |_            |_
   left_top  |_|           |_| right_top
             |             |
             |_            |_
left_bottom  |_|           |_| right_bottom
             |             |
             |_____________|
                |_|   |_|
        bottom_left   bottom_right

"""
mortises_on_top_tuple = ("top_left","top_right")
mortises_on_left_tuple = ("left_top","left_bottom")
tenons_on_right_tuple = ("right_top", "right_bottom")
tenons_on_bottom_tuple = ("bottom_left", "bottom_right")


# Dimensions for the tenons and mortises
""" top view showing W(idth) and L(ength) for tenon

  |-----|
  |_    |_
  |_|W  |_|W
  |L    |L
  |_____|

"""
tenon_width = piece_length / 10
tenon_length = tenon_width
tenon_height = piece_height / 2
mortise_width = tenon_width
mortise_length = tenon_length
mortise_height = tenon_height


# Organization of puzzle pieces from 0,0 point right and up (coordinate = right+up)
"""
naming of each piece resembles paper maps
example four by four grid

 DA DB DC DD
 CA CB CC CD
 BA BB BC BD
 AA AB AC AD
"""

def make_cube(name, x, y, z):
    obj = document.addObject("Part::Box", name)
    obj.Length = x
    obj.Width = y
    obj.Height = z
    document.recompute()
    return obj

def make_plane(name, length, width, posx, posy, posz, axx, axy, axz):
    """ make a plane of lenght and width; at position posx, posy, posz; using axises axx, axy, axz """
    c = document.addObject("Part::Plane", name)
    c.Length = length
    c.Width = width
    c.Placement = FreeCAD.Placement(FreeCAD.Vector(posx, posy, posz), FreeCAD.Rotation(FreeCAD.Vector(axx, axy, axz), 90))
    return c

# create document
if document is None:
    FreeCAD.newDocument(document_name)
    FreeCAD.setActiveDocument(document_name)
    document = FreeCAD.activeDocument()

# make base
piece = make_cube("piece", piece_length, piece_width, piece_height)

# place base
document.piece.Placement = FreeCAD.Placement(Vector(0, 0, 0), FreeCAD.Rotation(0, 0, 0), Vector(0, 0, 0))


# make and place tenons on the right
for i in range(len(tenons_on_right_tuple)):
    name = "tenon_" + tenons_on_right_tuple[i]
    x = piece_length
    y = (piece_length / 4) * (i * 2 + 1) - (tenon_width / 2)
    z = 1
    tenon = make_cube(name, tenon_length, tenon_width, tenon_height)
    tenon.Placement = FreeCAD.Placement(Vector(x, y, z), FreeCAD.Rotation(0,0,0), Vector(0,0,0))

# make and place tenons on the bottom
for i in range(len(tenons_on_bottom_tuple)):
    name = "tenon_" + tenons_on_bottom_tuple[i]
    x = (piece_length / 4) * (i * 2 + 1) - (tenon_width / 2)
    y = - tenon_length
    z = 1
    tenon = make_cube(name, tenon_length, tenon_width, tenon_height)
    tenon.Placement = FreeCAD.Placement(Vector(x, y, z), FreeCAD.Rotation(0,0,0), Vector(0,0,0))

# make and place mortises on the top
for i in range(len(mortises_on_top_tuple)):
    name = "mortise_" + mortises_on_top_tuple[i]
    x = (piece_length / 4) * (i * 2 + 1) - (mortise_width / 2)
    y = piece_length - mortise_length
    z = 1
    mortise = make_cube(name, mortise_length, mortise_width, mortise_height)
    mortise.Placement = FreeCAD.Placement(Vector(x, y, z), FreeCAD.Rotation(0,0,0), Vector(0,0,0))

# make and place mortises on the left
for i in range(len(mortises_on_left_tuple)):
    name = "mortise_" + mortises_on_left_tuple[i]
    x = 0
    y = (piece_length / 4) * (i * 2 + 1) - (mortise_width / 2)
    z = 1
    mortise = make_cube(name, mortise_length, mortise_width, mortise_height)
    mortise.Placement = FreeCAD.Placement(Vector(x, y, z), FreeCAD.Rotation(0,0,0), Vector(0,0,0))


# make compound of all mortises
document.addObject("Part::Compound","mortises")
document.mortises.Links = [document.mortise_top_right, document.mortise_top_left, document.mortise_left_top, document.mortise_left_bottom]

# join piece with tenons
j = BOPTools.JoinFeatures.makeConnect(name='piece_and_tenons')
j.Objects = [document.piece, document.tenon_right_top, document.tenon_right_bottom, document.tenon_bottom_left, document.tenon_bottom_right]
j.Proxy.execute(j)
#j.purgeTouched()
#for obj in j.ViewObject.Proxy.claimChildren():
#    obj.ViewObject.hide()
#j.ViewObject.hide()

# cutout piece with mortises
j = BOPTools.JoinFeatures.makeCutout(name='piece_template')
j.Base = document.piece_and_tenons
j.Tool = document.mortises
j.Proxy.execute(j)
#j.purgeTouched()
#for obj in j.ViewObject.Proxy.claimChildren():
#    obj.ViewObject.hide()
#j.ViewObject.hide()

#document.recompute()

# loop creating copies in grid
abc = "abcdefghijklmnopqrstuvwxyz"
offset = piece_length + piece_separation

for i in range(rows):
    for j in range(cols):
        current_label = "piece_" + abc[i] + abc[j]
        obj = document.addObject('Part::Feature','piece_template')
        obj.Shape = document.piece_template.Shape
        obj.Label = current_label
        obj.Placement = FreeCAD.Placement(Vector(offset * j, - offset * i - piece_length, 0), FreeCAD.Rotation(0,0,0), Vector(0,0,0))


# remove obsolete objects
document.removeObject('piece')
document.removeObject('piece_template')
document.removeObject('piece_and_tenons')
document.removeObject('mortises')
document.removeObject('tenon_right_top')
document.removeObject('tenon_right_bottom')
document.removeObject('tenon_bottom_left')
document.removeObject('tenon_bottom_right')
document.removeObject('mortise_top_left')
document.removeObject('mortise_top_right')
document.removeObject('mortise_left_top')
document.removeObject('mortise_left_bottom')


# import svg file
# -- SVG created with Maperitive to correct size
# -- then edited with Inkscape to remove redundant layers
# -- then edited with vi to remove <g> and <text> and the rect
importSVG.insert(svg_filename,"Scripted")

# convert all path to pipe
for obj in FreeCAD.ActiveDocument.Objects:
    if obj.Name.find("path")!=-1:
        obj.Placement = FreeCAD.Placement(Vector(-10.00,0.00,4.00),FreeCAD.Rotation(Vector(0.00,0.00,1.00),0.00))
        Arch.makePipe(obj, diameter = 2.5)
        print(obj.Label)

document.recompute()


# create planes for cutting
plane1 = make_plane("plane1", 20, 600,   0, -500, 4, 0, -1, 0)
plane2 = make_plane("plane2", 20, 600, 200, -500, 4, 0, -1, 0)
plane3 = make_plane("plane3", 20, 600, 400, -500, 4, 0, -1, 0)

plane4 = make_plane("plane4", 600, 20, 0, 0, 4, 1, 0, 0)
plane5 = make_plane("plane5", 600, 20, 0, -200, 4, 1, 0, 0)
plane6 = make_plane("plane6", 600, 20, 0, -400, 4, 1, 0, 0)


