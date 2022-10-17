"""
surfaces.py
Paul Cobbaut, 2022-10-17
The goal is to make several distinct surfaces to mark spots on a map for blind people.
"""

import FreeCAD
from FreeCAD import Base, Vector
from BasicShapes import Shapes
import Part
import Sketcher
import Draft
import math

# FreeCAD document
doc = FreeCAD.newDocument("Surfaces scripted")
obj = doc.addObject("PartDesign::Body", "Body")


# create a template dot
def create_template_dot(radius, name):
    dot = doc.addObject("Part::Sphere", name)
    dot.Radius = radius
    dot.Angle1 = -90
    dot.Angle2 = 90
    dot.Angle3 = 180
    dot.Placement = FreeCAD.Placement(Vector(0, 0, 0), FreeCAD.Rotation(180, 0, 90))

# create a template tube
def create_template_tube(height, radius, name):
    tube = Shapes.addTube(doc, name)
    tube.Height = height
    tube.InnerRadius = 0
    tube.OuterRadius = radius
    tube.Placement = FreeCAD.Placement(Vector(0, 0, 0), FreeCAD.Rotation(180, 0, 90))


def create_dotted_grid(x_mm, y_mm, radius):
    create_template_dot(radius, "dot")
    x_space_mm = 2 + radius
    y_space_mm = 2 + radius
    x_count = math.floor(x_mm / x_space_mm)
    y_count = math.floor(y_mm / y_space_mm)
    for j in range(y_count):
        y = j * y_space_mm
        for i in range(x_count):
            x = i * x_space_mm
            obj = doc.addObject('Part::Feature','dot')
            obj.Shape = doc.dot.Shape
            obj.Label = "dot_" + str(x) + "_" + str(y)		# name has 'some' meaning: dot + character position + Braille dot
            obj.Placement = FreeCAD.Placement(Vector(x, y, 0), FreeCAD.Rotation(180, 0, 90))
            doc.recompute()

def create_tubed_grid(x_mm, y_mm, radius):
    create_template_tube(y_mm, radius, "tube")
    x_space_mm = 2 + radius
    x_count = math.floor(x_mm / x_space_mm)
    for i in range(x_count):
        x = i * x_space_mm
        obj = doc.addObject('Part::Feature','tube')
        obj.Shape = doc.tube.Shape
        obj.Label = "tube_" + str(x)
        obj.Placement = FreeCAD.Placement(Vector(x, 0, 0), FreeCAD.Rotation(180, 0, 90))
        doc.recompute()


def main():
#    create_dotted_grid(40, 80, 7)
    create_tubed_grid(40, 80, 3)

    doc.recompute()
    FreeCADGui.ActiveDocument.ActiveView.fitAll()

main()
