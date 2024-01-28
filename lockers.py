"""
lockers.py -- Paul Cobbaut, 2024-01-27
Create keychains for lockers used by blind people
"""

# Dimensions
disc_radius_mm = 21
disc_height_mm = 2
hole_radius_mm = 2

# Numbers
lockers = 23 # the number of lockers
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
def make_tophalf_template():
    # get the half disc
    tophalf = make_half_disc("tophalf")
    # extrude text MARKGRAVE
    MARKGRAVE = create_wmstring("MARKGRAVE")
    xpos = -13  # hardcoded...
    ypos = -13
    zpos = disc_height_mm/2
    MARKGRAVE.Placement = FreeCAD.Placement(Vector(xpos, ypos, zpos), FreeCAD.Rotation(0,0,0), Vector(0,0,0))
    # extrude text VZW
    VZW       = create_wmstring("VZW")
    xpos = 1 - disc_radius_mm/4
    ypos = 3 - disc_radius_mm
    zpos = disc_height_mm/2
    VZW.Placement = FreeCAD.Placement(Vector(xpos, ypos, zpos), FreeCAD.Rotation(0,0,0), Vector(0,0,0))
    # create compound of the half disc and the extruded texts
    compound_list = []
    compound_list.append(tophalf)
    compound_list.append(MARKGRAVE)
    compound_list.append(VZW)
    tophalf_template = doc.addObject("Part::Compound", "tophalf_template")
    tophalf_template.Links = compound_list
    # cleanup
    tophalf.ViewObject.hide()
    MARKGRAVE.ViewObject.hide()
    VZW.ViewObject.hide()
    return tophalf_template

def make_bothalf_template():
    bothalf_template = make_half_disc("bothalf_template")
    xpos = 0
    ypos = - separation_mm
    zpos = disc_height_mm/2
    bothalf_template.Placement = FreeCAD.Placement(Vector(xpos, ypos, zpos), FreeCAD.Rotation(0,0,0), Vector(0,0,0))
    return bothalf_template

def make_half_disc(name):
    # halves start as a cylinder
    cyl = doc.addObject("Part::Cylinder", name + "_cyl")
    cyl.Radius = disc_radius_mm
    cyl.Height = disc_height_mm/2
    # fillet the top edge
    disc = doc.addObject("Part::Fillet",name + "_disc")
    disc.Base = cyl
    edges = []
    edges.append((3,0.99,0.99))
    disc.Edges = edges
    # the hole is a cylinder
    hole = doc.addObject("Part::Cylinder", name + "_hole")
    hole.Radius = hole_radius_mm
    hole.Height = disc_height_mm/2
    hole.Placement = FreeCAD.Placement(Vector(0, 3*(disc_radius_mm/4), 0), FreeCAD.Rotation(0,0,0), Vector(0,0,0))
    # cut the hole from the disc
    half_template = doc.addObject('Part::Cut', name)
    f = doc.getObject(name)
    f.Base = disc
    f.Tool = hole
    f.Label = name
    # clean up
    hole.ViewObject.hide()
    cyl.ViewObject.hide()
    disc.ViewObject.hide()
    doc.recompute()
    return f


def create_wmstring(text):
    # hardcoded value
    font_size = 1.5
    # create string containing watermark
    wmstring=Draft.make_shapestring(String=text, FontFile=font_file, Size=font_size, Tracking=0.0)
    #xpos = 0
    #ypos = 0
    #zpos = disc_height_mm/2
    #wmstring.Placement = FreeCAD.Placement(Vector(xpos, ypos, zpos), FreeCAD.Rotation(0,0,0), Vector(0,0,0))
    wmstring.Support=None
    wmstring.Label=text + '_string'
    Draft.autogroup(wmstring)
    # extrude the shapestring
    emboss = doc.addObject('Part::Extrusion',text + '_emboss')
    f = doc.getObject(text + '_emboss')
    f.Base = wmstring
    f.DirMode = "Normal"
    f.DirLink = None
    f.LengthFwd = 0.50
    f.LengthRev = 0
    f.Solid = False
    f.Reversed = False
    f.Symmetric = False
    f.TaperAngle = 0
    f.TaperAngleRev = 0
    f.Label=text
    doc.recompute()
    wmstring.ViewObject.hide()
    return f


def create_halves():
    # hardcoded values for the numbers on tophalves
    font_size = 10
    font_offset = 7
    # copy the half template for each locker, twice (both halves)
    for i in range(int(lockers)):
        # copy tophalf template
        tophalf = doc.addObject('Part::Feature','tophalf')
        tophalf.Shape = doc.tophalf_template.Shape
        tophalf.Label = "tophalf_" + str(i+1) 
        # position tophalf copy in FreeCAD GUI
        xpos = (i+1) * separation_mm
        ypos = separation_mm
        tophalf.Placement = FreeCAD.Placement(Vector(xpos, ypos, 0), FreeCAD.Rotation(0,0,0), Vector(0,0,0))
        # create a shapestring
        sname = 'string_' + str(i+1)              # name of the shapestring
        ename = 'string_' + str(i+1) + '_extrude' # name of the extrude
        newstring=Draft.make_shapestring(String=str(i+1), FontFile=font_file, Size=font_size, Tracking=0.0)
        # position the shapestring (shift double digit numbers to the left)
        if (i<9):
            xpos = (i+1) * separation_mm
        else:
            xpos = (i+1) * separation_mm - 15
        ypos = separation_mm - font_offset
        zpos = disc_height_mm/2
        newstring.Placement = FreeCAD.Placement(Vector(xpos, ypos, zpos), FreeCAD.Rotation(0,0,0), Vector(0,0,0))
        newstring.Support = None
        newstring.Label = sname
        Draft.autogroup(newstring)
        # extrude the shapestring
        newextrude = doc.addObject('Part::Extrusion',ename)
        f = doc.getObject(ename)
        f.Base = newstring
        f.DirMode = "Normal"
        f.DirLink = None
        f.LengthFwd = 1
        f.LengthRev = 0
        f.Solid = False
        f.Reversed = False
        f.Symmetric = False
        f.TaperAngle = 0
        f.TaperAngleRev = 0
        f.Label = ename
        # compund extrusion with tophalf
        tmp_compound = []
        tmp_compound.append(tophalf)
        tmp_compound.append(f)
        obj = doc.addObject("Part::Compound", 'topcompound_' + str(i+1))
        obj.Links = tmp_compound
        obj.Label = 'topcompound_' + str(i+1)
        # copy bottomhalf template
        bothalf = doc.addObject('Part::Feature','bothalf')
        bothalf.Shape = doc.bothalf_template.Shape
        bothalf.Label = "bothalf_" + str(i+1) 
        # position bottomhalf copy in FreeCAD GUI
        xpos = (i+1) * separation_mm
        ypos = - separation_mm
        bothalf.Placement = FreeCAD.Placement(Vector(xpos, ypos, 0), FreeCAD.Rotation(0,0,0), Vector(0,0,0))
        # braille string
        braille_string = print_braille_string(str(i+1), 0)
        # position the braillestring (shift double digit numbers to the left)
        if (i<9):
            xpos = (i+1) * separation_mm - 20
        else:
            xpos = (i+1) * separation_mm - 30
        ypos = - 5 - separation_mm
        zpos = disc_height_mm/2
        braille_string.Placement = FreeCAD.Placement(Vector(xpos, ypos, zpos), FreeCAD.Rotation(0,0,0), Vector(0,0,0))
    doc.recompute()
    return


###########
# Braille #
###########

# These four define the size of the dots in mmm
dot_size = 1.5       # diameter of a dot
dot_separation = 5   # space between center of dots
char_separation = 14 # space between center of characters
line_separation = 32 # space between center of lines

# Braille alphabet
# List of supported characters
"""
a 	⠁ 	1
b 	⠃ 	12
c 	⠉ 	14
d 	⠙ 	145
e 	⠑ 	15
f 	⠋ 	124
g 	⠛ 	1245
h 	⠓ 	125
i 	⠊ 	24
j 	⠚ 	245
k 	⠅ 	13
l 	⠇ 	123
m 	⠍ 	134
n 	⠝ 	1345
o 	⠕ 	135
p 	⠏ 	1234
q 	⠟ 	12345
r 	⠗ 	1235
s 	⠎ 	234
t 	⠞ 	2345
u 	⠥ 	136
v 	⠧ 	1236
w 	⠺ 	2456
x 	⠭ 	1346
y 	⠽ 	13456
z 	⠵ 	1356
number indicator 	⠼ 	3456
1 	⠼⠁ 	3456 1
2 	⠼⠃ 	3456 12
3 	⠼⠉ 	3456 14
4 	⠼⠙ 	3456 145
5 	⠼⠑ 	3456 15
6 	⠼⠋ 	3456 124
7 	⠼⠛ 	3456 1245
8 	⠼⠓ 	3456 125
9 	⠼⠊ 	3456 24
0 	⠼⠚ 	3456 245
"""

# dictionary character : dots printed
braille = {
  "a" : "1",
  "b" : "12",
  "c" : "14",
  "d" : "145",
  "e" : "15",
  "f" : "124",
  "g" : "1245",
  "h" : "125",
  "i" : "24",
  "j" : "245",
  "k" : "13",
  "l" : "123",
  "m" : "134",
  "n" : "1345",
  "o" : "135",
  "p" : "1234",
  "q" : "12345",
  "r" : "1235",
  "s" : "234",
  "t" : "2345",
  "u" : "136",
  "v" : "1236",
  "w" : "2456",
  "x" : "1346",
  "y" : "13456",
  "z" : "1356",
  "1" : "1",
  "2" : "12",
  "3" : "14",
  "4" : "145",
  "5" : "15",
  "6" : "124",
  "7" : "1245",
  "8" : "125",
  "9" : "24",
  "0" : "245",
  " " : "",
  "-" : "36"
}


# create the template dot that is always copied
def create_template_dot():
    dot = doc.addObject("Part::Sphere", "dot")
    dot.Radius = dot_size
    dot.Angle1 = -90
    dot.Angle2 = 90
    dot.Angle3 = 180
    dot.Placement = FreeCAD.Placement(Vector(0, 0, 0), FreeCAD.Rotation(180, 0, 90))
    dot.ViewObject.hide()
    doc.recompute()	# This seems needed, otherwise nothing appears in FreeCAD


# place a dot in the correct position
def place_a_dot(dot_number, char_count, line_count):		# dot_number is Braille dot 1, 2, 3, 4, 5 or 6
    obj = doc.addObject('Part::Feature','dot')			# copy the template dot
    obj.Shape = doc.dot.Shape
    obj.Label = "dot_" + str(line_count) + "_" + str(char_count) + "_" + str(dot_number)	# name has 'some' meaning: dot + character position + Braille dot
    # Get X coordinate
    left_right = dot_number >> 2				# 0 if 1,2 or 3, 1 if 4, 5 or 6 (zero means dot on the left, one means dot on the right)
    char_position = char_count * char_separation		# this is the n-th character (n = char_count + 1 )
    dot_position = dot_separation * left_right                  # this is either a 123 dot on the left, or a 456 dot on the right
    x = char_position + dot_position
    # Get Y coordinate
    line_position = line_separation * line_count
    y = dot_separation * (- dot_number % 3) - line_position	# negative modulo 3 gives Y coordinate (three dots above each other)
    # Finale position for this dot
    position = FreeCAD.Vector(x, y, 0)
    rotation = FreeCAD.Rotation(180, 0, 90)
    obj.Placement = FreeCAD.Placement(position, rotation)	# put copied and named dot in correct location
    return obj


# prints one Braille string
def print_braille_string(string, line_count):
    # keeps track of the n-th character on each line
    # is used for the position of the current character
    char_count = 0
    # list te create compound when string is written
    compound_list = []
    # when this is True, then put no 'Number Indicator' in Braille
    previous_is_digit = False
    for letter in string:
        char_count = char_count + 1
        if letter.isdigit():
            if previous_is_digit == False:
                previous_is_digit = True
                # Braille Number Indicator = "3456"
                obj = place_a_dot(3, char_count, line_count)
                compound_list.append(obj)
                obj = place_a_dot(4, char_count, line_count)
                compound_list.append(obj)
                obj = place_a_dot(5, char_count, line_count)
                compound_list.append(obj)
                obj = place_a_dot(6, char_count, line_count)
                compound_list.append(obj)
                char_count = char_count + 1
        else:
            previous_is_digit = False
        for i in range(1,7):
            if str(i) in braille[letter]:
                obj = place_a_dot(i, char_count, line_count)
                compound_list.append(obj)
    line_name = "line_" + string
    obj = doc.addObject("Part::Compound",line_name)
    obj.Links = compound_list
    doc.recompute()	# This seems needed, otherwise nothing appears in FreeCAD
    return obj

#########
# Start #
#########

# create a FreeCAD document 
doc               = FreeCAD.newDocument("Blindenlockers generated")
tophalf_template  = make_tophalf_template()
bothalf_template  = make_bothalf_template()
create_template_dot()
create_halves()
print_braille_string("23", 0)

##doc.removeObject("loft")
# show in GUI
doc.recompute()
FreeCADGui.ActiveDocument.ActiveView.fitAll()
