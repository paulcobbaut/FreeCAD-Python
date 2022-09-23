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
obj = doc.addObject("PartDesign::Body", "Body")
#obj.Label = "custom name for body"

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
piece_length = 180               # X-coordinate in FreeCAD
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

# create a sketch with dovetails and pockets that will be padded later
sketch = doc.getObject('Body').newObject("Sketcher::SketchObject", "Sketch")



# start drawing piece at origin
# first part draws left side
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
y = (piece_length * 3 / 4) - (dove_width / 2)
sketch.addGeometry(Part.LineSegment(App.Vector(px, py, 0), App.Vector(x, y, 0)), False)

# left_top dovetail
px = x
py = y
x = 0 - dove_length
y = (piece_length * 3 / 4) - (dove_width / 2) - dove_side
sketch.addGeometry(Part.LineSegment(App.Vector(px, py, 0), App.Vector(x, y, 0)), False)

px = x
py = y
x = 0 - dove_length
y = (piece_length * 3 / 4) - (dove_width / 2) + dove_width + dove_side
sketch.addGeometry(Part.LineSegment(App.Vector(px, py, 0), App.Vector(x, y, 0)), False)

px = x
py = y
x = 0
y = (piece_length * 3 / 4) - (dove_width / 2) + dove_width
sketch.addGeometry(Part.LineSegment(App.Vector(px, py, 0), App.Vector(x, y, 0)), False)

# side to top
px = x
py = y
x = 0
y = piece_length
sketch.addGeometry(Part.LineSegment(App.Vector(px, py, 0), App.Vector(x, y, 0)), False)


# copy complete left side and place at opposite side
doc.getObject('Sketch').addCopy([0,1,2,3,4,5,6,7,8], App.Vector(piece_length, 0, 0), True)



# start drawing piece at origin
# first part draws bottom side
x = 0
y = (piece_length / 4) - (dove_width / 2)
sketch.addGeometry(Part.LineSegment(App.Vector(0, 0, 0), App.Vector(y, x, 0)), False)

# bottom_left dovetail
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
y = (piece_length * 3 / 4) - (dove_width / 2)
sketch.addGeometry(Part.LineSegment(App.Vector(py, -px, 0), App.Vector(y, -x, 0)), False)

# bottom_right pocket
px = x
py = y
x = 0 - dove_length
y = (piece_length * 3 / 4) - (dove_width / 2) - dove_side
sketch.addGeometry(Part.LineSegment(App.Vector(py, -px, 0), App.Vector(y, -x, 0)), False)

px = x
py = y
x = 0 - dove_length
y = (piece_length * 3 / 4) - (dove_width / 2) + dove_width + dove_side
sketch.addGeometry(Part.LineSegment(App.Vector(py, -px, 0), App.Vector(y, -x, 0)), False)

px = x
py = y
x = 0
y = (piece_length * 3 / 4) - (dove_width / 2) + dove_width
sketch.addGeometry(Part.LineSegment(App.Vector(py, -px, 0), App.Vector(y, -x, 0)), False)

# side to far right
px = x
py = y
x = 0
y = piece_length
sketch.addGeometry(Part.LineSegment(App.Vector(py, -px, 0), App.Vector(y, -x, 0)), False)

# copy and place at opposite (top) side
doc.getObject('Sketch').addCopy([18,19,20,21,22,23,24,25,26], App.Vector(0, piece_length, 0), True)


# pad this sketch
pad = doc.getObject('Body').newObject("PartDesign::Pad", "Pad")
pad.Profile = doc.getObject("Sketch")
pad.Length = 2

#
# we now have an empty piece with dovetails and pockets that fits with itself
#

# start putting braille on it



"""
braille.py
Paul Cobbaut, 2022-07-05
FreeCAD Braille font
This script parses text and converts it to Braille dots in FreeCAD
"""


# position of Braille dots
"""
14
25
36
"""


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
  " " : ""
}

# These four define the size of the dots in mmm
dot_size = .5          # diameter of a dot
dot_separation = 2.5   # space between center of dots
char_separation = 6.4  # space between center of characters
line_separation = 32   # space between center of lines


# create the template dot that is always copied
def create_template_dot(dotname):
    tdot = doc.addObject("Part::Sphere", dotname)
    tdot.Radius = dot_size
    tdot.Angle1 = -90
    tdot.Angle2 = 90
    tdot.Angle3 = 180
    tdot.Placement = FreeCAD.Placement(Vector(0, 0, 0), FreeCAD.Rotation(180, 0, 90))
    tdot.ViewObject.hide()
    doc.recompute()	# This seems needed, otherwise nothing appears in FreeCAD


# place a dot in the correct position
def place_a_dot(dot_number, char_count, line_count, dotname):		# dot_number is Braille dot 1, 2, 3, 4, 5 or 6
    obj = doc.addObject('Part::Feature', dotname)			# copy the template dot
    obj.Shape = doc.getObject(dotname).Shape
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
    pad_height = 2
    position = FreeCAD.Vector(x, y, pad_height)
    rotation = FreeCAD.Rotation(180, 0, 90)
    obj.Placement = FreeCAD.Placement(position, rotation)	# put copied and named dot in correct location
    return obj


# prints one Braille string
def print_braille_string(string, line_count, dotname):
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
                obj = place_a_dot(3, char_count, line_count, dotname)
                compound_list.append(obj)
                obj = place_a_dot(4, char_count, line_count, dotname)
                compound_list.append(obj)
                obj = place_a_dot(5, char_count, line_count, dotname)
                compound_list.append(obj)
                obj = place_a_dot(6, char_count, line_count, dotname)
                compound_list.append(obj)
                char_count = char_count + 1
        else:
            previous_is_digit = False
        for i in range(1,7):
            if str(i) in braille[letter]:
                obj = place_a_dot(i, char_count, line_count, dotname)
                compound_list.append(obj)
    line_name = "line_" + str(line_count)
    obj = doc.addObject("Part::Compound",line_name)
    obj.Links = compound_list
    doc.recompute()	# This seems needed, otherwise nothing appears in FreeCAD


# program starts here
def main():
    global dot_size
    global dot_separation
    global char_separation
    global line_separation

    # line_count keeps track of the n-th line
    # is used for the position of the current line
    line_count = 0

    # change dot diameter, nothing else
    # dot1
    dot_size = .2          # diameter of a dot
    dot_separation = 2.5   # space between center of dots
    char_separation = 6.4  # space between center of characters
    line_separation = 14   # space between center of lines
    create_template_dot("dot1")
    print_braille_string("punt twintig", line_count, "dot1")
    line_count = line_count + 1

    # dot2
    dot_size = .3          # diameter of a dot
    dot_separation = 2.5   # space between center of dots
    char_separation = 6.4  # space between center of characters
    create_template_dot("dot2")
    print_braille_string("punt dertig", line_count, "dot2")
    line_count = line_count + 1

    # dot3
    dot_size = .4          # diameter of a dot
    dot_separation = 2.5   # space between center of dots
    char_separation = 6.4  # space between center of characters
    create_template_dot("dot3")
    print_braille_string("punt veertig", line_count, "dot3")
    line_count = line_count + 1

    # dot4
    dot_size = .5          # diameter of a dot
    dot_separation = 2.5   # space between center of dots
    char_separation = 6.4  # space between center of characters
    create_template_dot("dot4")
    print_braille_string("punt vijftig", line_count, "dot4")
    line_count = line_count + 1

    # dot5
    dot_size = .6          # diameter of a dot
    dot_separation = 2.5   # space between center of dots
    char_separation = 6.4  # space between center of characters
    create_template_dot("dot5")
    print_braille_string("punt zestig", line_count, "dot5")
    line_count = line_count + 1

    # dot6
    dot_size = .7          # diameter of a dot
    dot_separation = 2.5   # space between center of dots
    char_separation = 6.4  # space between center of characters
    create_template_dot("dot6")
    print_braille_string("punt zeventig", line_count, "dot6")
    line_count = line_count + 1



    # alles .5 en afstand aanpassen
    # dot7
    dot_size = .5          # diameter of a dot
    dot_separation = 2     # space between center of dots
    char_separation = 5    # space between center of characters
    create_template_dot("dot7")
    print_braille_string("dichtst bij elkaar", line_count, "dot7")
    line_count = line_count + 1

    # dot8
    dot_size = .5          # diameter of a dot
    dot_separation = 2.2   # space between center of dots
    char_separation = 5.5  # space between center of characters
    create_template_dot("dot8")
    print_braille_string("dicht bij elkaar", line_count, "dot8")
    line_count = line_count + 1

    # dot9
    dot_size = .5          # diameter of a dot
    dot_separation = 2.4   # space between center of dots
    char_separation = 6    # space between center of characters
    create_template_dot("dot9")
    print_braille_string("net te dicht", line_count, "dot9")
    line_count = line_count + 1

    # dot10
    dot_size = .5          # diameter of a dot
    dot_separation = 2.6   # space between center of dots
    char_separation = 6.5  # space between center of characters
    create_template_dot("dot10")
    print_braille_string("net te ver", line_count, "dot10")
    line_count = line_count + 1

    # dot11
    dot_size = .5          # diameter of a dot
    dot_separation = 2.8   # space between center of dots
    char_separation = 7    # space between center of characters
    create_template_dot("dot11")
    print_braille_string("verder weg", line_count, "dot11")
    line_count = line_count + 1

    # dot12
    dot_size = .5          # diameter of a dot
    dot_separation = 3   # space between center of dots
    char_separation = 7.5  # space between center of characters
    create_template_dot("dot12")
    print_braille_string("veel te ver", line_count, "dot12")
    line_count = line_count + 1


    # character separation
    # dot13
    dot_size = .5          # diameter of a dot
    dot_separation = 2.5   # space between center of dots
    char_separation = 8    # space between center of characters
    create_template_dot("dot13")
    print_braille_string("samen sterk", line_count, "dot13")
    line_count = line_count + 1

    # dot14
    dot_size = .5          # diameter of a dot
    dot_separation = 2.5   # space between center of dots
    char_separation = 10   # space between center of characters
    create_template_dot("dot14")
    print_braille_string("kleine afstand", line_count, "dot14")
    line_count = line_count + 1

    # dot15
    dot_size = .5          # diameter of a dot
    dot_separation = 2.5   # space between center of dots
    char_separation = 12   # space between center of characters
    create_template_dot("dot15")
    print_braille_string("corona veilig", line_count, "dot15")
    line_count = line_count + 1

    # dot16
    dot_size = .5          # diameter of a dot
    dot_separation = 2.5   # space between center of dots
    char_separation = 14   # space between center of characters
    create_template_dot("dot16")
    print_braille_string("solitair", line_count, "dot16")
    line_count = line_count + 1


main()


doc.recompute()

FreeCADGui.ActiveDocument.ActiveView.fitAll()

