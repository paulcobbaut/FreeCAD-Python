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
|A/|          |A/|
|/ |          |/ |
   |W         |  |W
   |W         |  |W
|\ |          |\ |
| \|          | \|
|LLL          |LLL     
|             |  
|-------------|

"""
dove_width = piece_length / 20
dove_length = piece_length / 40
#angle = 30
dove_hyp = 2 * dove_length       # Hypotenuse at 30 degree angle
dove_side = 1.732 * dove_length  # other side at 30 degree angle




sketch = doc.addObject("Sketcher::SketchObject", "Sketch")



#sketch.addGeometry(Part.LineSegment(App.Vector(0, 0, 0), App.Vector(s, w, 0)), False)
#sketch.addGeometry(Part.LineSegment(App.Vector(s, w, 0), App.Vector(s + l, w, 0)), False)
#sketch.addGeometry(Part.LineSegment(App.Vector(s + l, w, 0), App.Vector(s + s + l, 0, 0)), False)
#sketch.addGeometry(Part.LineSegment(App.Vector(s + s + l, 0, 0), App.Vector(0, 0, 0)), False)


# start drawing piece at origin
x = 0
y = (piece_length / 4) - (dove_width / 2)
sketch.addGeometry(Part.LineSegment(App.Vector(0, 0, 0), App.Vector(x, y, 0)), False)

# left_bottom pocket
px = x
py = y
x = dove_length
y = (piece_length / 4) - (dove_width / 2)  - dove_side
sketch.addGeometry(Part.LineSegment(App.Vector(px, py, 0), App.Vector(x, y, 0)), False)

px = x
py = y
x = dove_length
y = (piece_length / 4) - (dove_width / 2) + dove_width + dove_side
sketch.addGeometry(Part.LineSegment(App.Vector(px, py, 0), App.Vector(x, y, 0)), False)

px = x
py = y
x = 0
y = (piece_length / 4) - (dove_width / 2) + dove_width 
sketch.addGeometry(Part.LineSegment(App.Vector(px, py, 0), App.Vector(x, y, 0)), False)

# side middle
px = x
py = y
x = 0
y = (piece_length * 3 / 4) + (dove_width / 2)
sketch.addGeometry(Part.LineSegment(App.Vector(px, py, 0), App.Vector(x, y, 0)), False)

# left_top dovetail
px = x
py = y
x = 0 - dove_length
y = (piece_length * 3 / 4) + (dove_width / 2) - dove_side
sketch.addGeometry(Part.LineSegment(App.Vector(px, py, 0), App.Vector(x, y, 0)), False)

px = x
py = y
x = 0 - dove_length
y = (piece_length * 3 / 4) + (dove_width / 2) + dove_width + dove_side
sketch.addGeometry(Part.LineSegment(App.Vector(px, py, 0), App.Vector(x, y, 0)), False)

px = x
py = y
x = 0
y = (piece_length * 3 / 4) + (dove_width / 2) + dove_width
sketch.addGeometry(Part.LineSegment(App.Vector(px, py, 0), App.Vector(x, y, 0)), False)

# side to top
px = x
py = y
x = 0
y = piece_length
sketch.addGeometry(Part.LineSegment(App.Vector(px, py, 0), App.Vector(x, y, 0)), False)

# copy and place at opposite side
doc.getObject('Sketch').addCopy([0,1,2,3,4,5,6,7,8], App.Vector(piece_length, 0, 0), True)




# bottom 

# start drawing piece at origin
x = 0
y = (piece_length / 4) - (dove_width / 2)
sketch.addGeometry(Part.LineSegment(App.Vector(0, 0, 0), App.Vector(y, x, 0)), False)

# left_bottom pocket
px = x
py = y
x = dove_length
y = (piece_length / 4) - (dove_width / 2)  - dove_side
sketch.addGeometry(Part.LineSegment(App.Vector(py, -px, 0), App.Vector(y, -x, 0)), False)

px = x
py = y
x = dove_length
y = (piece_length / 4) - (dove_width / 2) + dove_width + dove_side
sketch.addGeometry(Part.LineSegment(App.Vector(py, -px, 0), App.Vector(y, -x, 0)), False)

px = x
py = y
x = 0
y = (piece_length / 4) - (dove_width / 2) + dove_width 
sketch.addGeometry(Part.LineSegment(App.Vector(py, -px, 0), App.Vector(y, -x, 0)), False)

# side middle
px = x
py = y
x = 0
y = (piece_length * 3 / 4) + (dove_width / 2)
sketch.addGeometry(Part.LineSegment(App.Vector(py, -px, 0), App.Vector(y, -x, 0)), False)

# left_top dovetail
px = x
py = y
x = 0 - dove_length
y = (piece_length * 3 / 4) + (dove_width / 2) - dove_side
sketch.addGeometry(Part.LineSegment(App.Vector(py, -px, 0), App.Vector(y, -x, 0)), False)

px = x
py = y
x = 0 - dove_length
y = (piece_length * 3 / 4) + (dove_width / 2) + dove_width + dove_side
sketch.addGeometry(Part.LineSegment(App.Vector(py, -px, 0), App.Vector(y, -x, 0)), False)

px = x
py = y
x = 0
y = (piece_length * 3 / 4) + (dove_width / 2) + dove_width
sketch.addGeometry(Part.LineSegment(App.Vector(py, -px, 0), App.Vector(y, -x, 0)), False)

# side to top
px = x
py = y
x = 0
y = piece_length
sketch.addGeometry(Part.LineSegment(App.Vector(py, -px, 0), App.Vector(y, -x, 0)), False)

# copy and place at opposite side
doc.getObject('Sketch').addCopy([18,19,20,21,22,23,24,25,26], App.Vector(0, piece_length, 0), True)






doc.recompute()


FreeCADGui.ActiveDocument.ActiveView.fitAll()


