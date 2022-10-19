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
    dot.ViewObject.hide()
    doc.recompute()

# create a template tube
def create_template_tube(height, radius, name):
    tube = Shapes.addTube(doc, name)
    tube.Height = height
    tube.InnerRadius = 0
    tube.OuterRadius = radius
    tube.Placement = FreeCAD.Placement(Vector(0, 0, 0), FreeCAD.Rotation(180, 0, 90))
    tube.ViewObject.hide()
    doc.recompute()


def create_dotted_grid(x_mm, y_mm, radius, dotspace):
    create_template_dot(radius, "dot")
    x_space_mm = dotspace + (radius * 2)
    y_space_mm = dotspace + (radius * 2)
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

def create_tubed_grid(x_mm, y_mm, radius, tubespace):
    create_template_tube(y_mm, radius, "tube")
    x_space_mm = tubespace + (radius * 2)
    x_count = math.floor(x_mm / x_space_mm)
    for i in range(x_count):
        x = i * x_space_mm
        obj = doc.addObject('Part::Feature','tube')
        obj.Shape = doc.tube.Shape
        obj.Label = "tube_" + str(x)
        obj.Placement = FreeCAD.Placement(Vector(x, 0, 0), FreeCAD.Rotation(180, 0, 90))
        doc.recompute()


def create_tubed_dirg(x_mm, y_mm, radius, tubespace):
    create_template_tube(x_mm, radius, "dirg")
    y_space_mm = tubespace + (radius * 2)
    y_count = math.floor(y_mm / y_space_mm)
    for i in range(y_count):
        y = i * y_space_mm
        obj = doc.addObject('Part::Feature','dirg')
        obj.Shape = doc.dirg.Shape
        obj.Label = "dirgtube_" + str(y)
        obj.Placement = FreeCAD.Placement(Vector(0, y, 0), FreeCAD.Rotation(90, 0, 90))
        doc.recompute()


def create_tubed_matrix(x_mm, y_mm, radius):
    create_tubed_grid(x_mm, y_mm, radius)
    create_tubed_dirg(y_mm, x_mm, radius)
    

def main():
# choose ONE:
# create a dotted grid(x in mm, y in mm, dotradius, dotspace)
#    create_dotted_grid(12, 12, 1, 1)
#
# create a tubed grid (x in mm, y in mm, tuberadius, tubespace)
#    create_tubed_grid(30, 30, 2, 1)
#
# create a tubed_matrix(x in mm, y in mm, tuberadius, tubespace)
#   create_tubed_matrix(40, 40, 2, 1)
#
    doc.recompute()
    FreeCADGui.ActiveDocument.ActiveView.fitAll()

main()
