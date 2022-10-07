"""
hexagon.py
Paul Cobbaut, 2022-10-07
Some FreeCAD scripting
The goal is to make a hexagon pattern for pocketing.
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
hex_radius_mm = 3
hex_sides_mm = 0.866 * hex_radius_mm
hex_gap_mm = hex_radius_mm / 3

# create a sketch 
sketch = doc.getObject('Body').newObject("Sketcher::SketchObject", "Sketch")


#ProfileLib.RegularPolygon.makeRegularPolygon(doc.getObject('Sketch'),6,App.Vector(0,0,0),App.Vector(hex_sides_mm,hex_radius_mm/2,0),False)


def create_hexagon_grid(x_mm, y_mm):
    width = 2 * hex_radius_mm + hex_gap_mm
    x_count = int(x_mm / width)
    for i in range(x_count):
        ProfileLib.RegularPolygon.makeRegularPolygon(doc.getObject('Sketch'),6,App.Vector(i * width, 0, 0),App.Vector(hex_sides_mm + i*width,hex_radius_mm/2,0),False)
    

create_hexagon_grid(100, 50)


doc.recompute()

FreeCADGui.ActiveDocument.ActiveView.fitAll()
