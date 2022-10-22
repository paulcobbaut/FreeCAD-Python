"""
magicbox.py
Paul Cobbaut, 2022-10-22
Some FreeCAD scripting
The goal is to make nice magic box 100% with python.
"""

import FreeCAD
from FreeCAD import Base, Vector
import Part
import Sketcher
import ProfileLib.RegularPolygon
import math

# FreeCAD document
doc = FreeCAD.newDocument("Magicbox scripted")
obj = doc.addObject("PartDesign::Body", "Body")

# box sizes in mm
box_inner_length	= 66	# ~ number of sleeved cards that fit (66mm ~ 75 cards)
box_inner_width		= 51	# ~ card with sleeve width
box_inner_height	= 88	# height of the bottom box

wall_width	= 1	# thickness of the sides
bottom_width	= 1	# thickness of the bottom of the box
top_width	= 1	# thickness of the top of the lid

gap		= 0.5	# gap so the lid can slide over the box

lid_inner_width		= box_inner_width + wall_width + gap
lid_inner_length	= box_inner_length + wall_width + gap
lid_inner_height	= 15

offset	= box_inner_length + 2*wall_width + 10	# position the lid next to the box


# hexagon size
hex_radius_mm	= 4
hex_cevian_mm	= 0.866 * hex_radius_mm
gap_mm		= hex_radius_mm - 1


def create_cube(length, width, height, name):
    obj = doc.addObject("Part::Box", name)
    obj.Length = length
    obj.Width = width
    obj.Height = height
    return obj


def create_box_using_two_cubes():
    '''
    Create a cube, create a smaller cube inside, substract small cube form big one
    Do this both for box and for lid
    '''
    # Create the cubes
    outer_box = create_cube(box_inner_length + 2*wall_width	, box_inner_width + 2*wall_width, box_inner_height + bottom_width	, 'outer_box')
    inner_box = create_cube(box_inner_length			, box_inner_width		, box_inner_height			, 'inner_box')
    outer_lid = create_cube(lid_inner_length + 2*wall_width	, lid_inner_width + 2*wall_width, lid_inner_height + top_width		, 'outer_lid')
    inner_lid = create_cube(lid_inner_length			, lid_inner_width		, lid_inner_height			, 'inner_lid')

    # position the cubes
    outer_box.Placement = FreeCAD.Placement(Vector(0, 0, 0), FreeCAD.Rotation(0,0,0), Vector(0,0,0))
    inner_box.Placement = FreeCAD.Placement(Vector(wall_width, wall_width, bottom_width), FreeCAD.Rotation(0,0,0), Vector(0,0,0))
    outer_lid.Placement = FreeCAD.Placement(Vector(offset, 0, 0), FreeCAD.Rotation(0,0,0), Vector(0,0,0))
    inner_lid.Placement = FreeCAD.Placement(Vector(offset + wall_width, wall_width, top_width ), FreeCAD.Rotation(0,0,0), Vector(0,0,0))

    # fillet the box (round the edges)
    edges = []
    i = 1
    for edge in doc.outer_box.Shape.Edges:
        edges.append((i,1.00,1.00))
        i = i + 1
    outer_box_fil = doc.addObject("Part::Fillet", 'outer_box_fil')
    outer_box_fil.Base = doc.outer_box
    outer_box_fil.Edges = edges

    edges = []
    i = 1
    for edge in doc.inner_box.Shape.Edges:
        if (edge.Length) == (box_inner_height):
            edges.append((i,1.00,1.00))
        i = i + 1
    inner_box_fil = doc.addObject("Part::Fillet", 'inner_box_fil')
    inner_box_fil.Base = doc.inner_box
    inner_box_fil.Edges = edges

    # fillet the lid (round the edges)
    edges = []
    i = 1
    for edge in doc.outer_lid.Shape.Edges:
        edges.append((i,1.00,1.00))
        i = i + 1
    outer_lid_fil = doc.addObject("Part::Fillet", 'outer_lid_fil')
    outer_lid_fil.Base = doc.outer_lid
    outer_lid_fil.Edges = edges

    edges = []
    i = 1
    for edge in doc.inner_lid.Shape.Edges:
        if (edge.Length) == (lid_inner_height):
            edges.append((i,1.00,1.00))
        i = i + 1
    inner_lid_fil = doc.addObject("Part::Fillet", 'inner_lid_fil')
    inner_lid_fil.Base = doc.inner_lid
    inner_lid_fil.Edges = edges

    # substract the inners from the outers
    mtgbox = doc.addObject('Part::Cut', 'mtgbox')
    mtgbox.Base = outer_box_fil
    mtgbox.Tool = inner_box_fil
    outer_box.ViewObject.hide()
    inner_box.ViewObject.hide()
    mtglid = doc.addObject('Part::Cut', 'mtglid')
    mtglid.Base = outer_lid_fil
    mtglid.Tool = inner_lid_fil
    outer_lid.ViewObject.hide()
    inner_lid.ViewObject.hide()



def create_hexagon_grid(x_mm, y_mm):
    XZ = doc.getObject('Body').newObject("Sketcher::SketchObject", "XZ")
    XZ.Support = (doc.getObject('XZ_Plane'),[''])
    XZ.MapMode = 'FlatFace'
    XZ.Label = 'XZ'
    #XZ.MapMode = 'ObjectXZ'
    x_space_mm = 2 * hex_cevian_mm + gap_mm  # space needed by a hex and its empty space in the X-axis
    y_space_mm = 1.5 * hex_radius_mm + gap_mm  # space needed by a hex and its empty space in the X-axis	
    x_count = math.floor(x_mm / x_space_mm) - 1
    y_count = math.floor(y_mm / y_space_mm) - 1
    for j in range(y_count):
        o_y = j * y_space_mm
        r_y = j * y_space_mm + hex_radius_mm/2
        for i in range(x_count):
            if (j % 2) == 0:
                o_x = i * x_space_mm
                r_x = i * x_space_mm + hex_cevian_mm
                ProfileLib.RegularPolygon.makeRegularPolygon(doc.getObject('XZ'),6,App.Vector(o_x, o_y, 0),App.Vector(r_x, r_y, 0),False)
            else:
                o_x = i * x_space_mm + x_space_mm/2
                r_x = i * x_space_mm + hex_cevian_mm + x_space_mm/2
                if (i < (x_count-1)):
                    ProfileLib.RegularPolygon.makeRegularPolygon(doc.getObject('XZ'),6,App.Vector(o_x, o_y, 0),App.Vector(r_x, r_y,0),False)
    
    

create_box_using_two_cubes()
#create_hexagon_grid(box_inner_height *.95, box_inner_width * .95)
create_hexagon_grid(box_inner_length * .95, box_inner_height * .95)

doc.recompute()
FreeCADGui.ActiveDocument.ActiveView.fitAll()
