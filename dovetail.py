"""
dovetail.py
Paul Cobbaut, 2022-09-20
Some FreeCAD scripting
The goal is to make interlocking dovetail pieces
When that works the next goal is putting braille and roads on the pieces
"""

import FreeCAD
from FreeCAD import Base, Vector
#import Arch
#import Draft
import Part
import Sketcher
#import importSVG
#import BOPTools
#import BOPTools.JoinFeatures

# FreeCAD document
doc = FreeCAD.newDocument("Dovetail scripted")

# SVG file to be imported
# svg_filename = "/home/paul/drawing.svg"

# number of pieces in grid (max 25!)
# rows = 2
# cols = 2

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
piece_height = 2                 # Z-coordinate in FreeCAD
#piece_separation = piece_length / 5
#piece_separation = 0


# Names and tuples for the tails and pockets
""" top view

                    top_right
           top_left    _
             _________|_|___
             |  |_|        |
            _|            _|
  left_top |_|           |_| right_top
             |             |
             |_            |_
 left_bottom |_|           |_| right_bottom
             |         _   |
             |________|_|__|
                |_|
        bottom_left   bottom_right

"""
tails = ("top_right", "left_top", "right_bottom", "bottom_left")
pockets = ("top_left", "left_bottom", "right_top", "bottom_right")


# Dimensions for the tails and pockets
""" top view 

|-------------|
|             |
|             |
| /|          | /|
|/ |          |/ |
   |          |  |
|\ |          |\ |
| \|          | \|
|             |
|             |  
|-------------|


top view showing W(idth) and L(ength) and A(ngle)

|-------------|
|             |
|             |
|A/|W         |A/|W
|/ |W         |/ |W
   |W         |  |W
|\ |W         |\ |W
| \|W         | \|W
|LLL          |LLL     
|             |  
|-------------|

"""
width = piece_length / 10
length = width
angle = 30


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
    obj = doc.addObject("Part::Box", name)
    obj.Length = x
    obj.Width = y
    obj.Height = z
    doc.recompute()
    return obj


# make base
#piece = make_cube("piece", piece_length, piece_width, piece_height)

# place base
#doc.piece.Placement = FreeCAD.Placement(Vector(0, 0, 0), FreeCAD.Rotation(0, 0, 0), Vector(0, 0, 0))




sketch = doc.addObject("Sketcher::SketchObject", "Sketch")
sketch.addGeometry(Part.LineSegment(App.Vector(0, 0, 0),
                                    App.Vector(5, 5, 0)), False)
sketch.addGeometry(Part.LineSegment(App.Vector(5, 5, 0),
                                    App.Vector(10, 5, 0)), False)
sketch.addGeometry(Part.LineSegment(App.Vector(10, 5, 0),
                                    App.Vector(12, 0, 0)), False)
sketch.addGeometry(Part.LineSegment(App.Vector(12, 0, 0),
                                    App.Vector(0, 0, 0)), False)




doc.recompute()


FreeCADGui.ActiveDocument.ActiveView.fitAll()


