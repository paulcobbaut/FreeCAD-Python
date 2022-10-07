"""
hexagon.py
Paul Cobbaut, 2022-10-07
Some FreeCAD scripting
The goal is to make a hexagon pattern of a fixed size for pocketing.
It works, finished!
"""

import FreeCAD
from FreeCAD import Base, Vector
import Part
import Sketcher
import ProfileLib.RegularPolygon

# FreeCAD document
doc = FreeCAD.newDocument("Hexagon scripted")
obj = doc.addObject("PartDesign::Body", "Body")

# hexagon size
hex_radius_mm	= 3
hex_cevian_mm	= 0.866 * hex_radius_mm
gap_mm		= hex_radius_mm / 3

# create a sketch 
sketch = doc.getObject('Body').newObject("Sketcher::SketchObject", "Sketch")

def create_hexagon_grid(x_mm, y_mm):
    space_mm = 2 * hex_radius_mm + gap_mm  # space needed by a hex and its empty space around it
    x_count = int(x_mm / space_mm)
    y_count = int(y_mm / space_mm)
    for j in range(y_count):
        o_y = j * space_mm
        r_y = j * space_mm + hex_radius_mm/2
        for i in range(x_count):
            if (j % 2) == 0:
                o_x = i * space_mm
                r_x = i * space_mm + hex_cevian_mm
            else:
                o_x = i * space_mm + space_mm/2
                r_x = i * space_mm + hex_cevian_mm + space_mm/2
            ProfileLib.RegularPolygon.makeRegularPolygon(doc.getObject('Sketch'),6,App.Vector(o_x, o_y, 0),App.Vector(r_x, r_y, 0),False)
    

create_hexagon_grid(100, 50)

doc.recompute()
FreeCADGui.ActiveDocument.ActiveView.fitAll()
