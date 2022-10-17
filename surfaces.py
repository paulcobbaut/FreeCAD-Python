"""
surfaces.py
Paul Cobbaut, 2022-10-17
The goal is to make several distinct surfaces to mark spots on a map for blind people.
"""

import FreeCAD
import Part
import Sketcher
import Draft
import math

# FreeCAD document
doc = FreeCAD.newDocument("Surfaces scripted")
obj = doc.addObject("PartDesign::Body", "Body")


pts = []
radius = 5
for ii in range(0,720):
    pts.append(FreeCAD.Base.Vector(ii*math.pi/180,math.sin(ii*math.pi/180),0))

Draft.makeBSpline(pts)

doc.recompute()
FreeCADGui.ActiveDocument.ActiveView.fitAll()
