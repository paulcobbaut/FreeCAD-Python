"""
dovetail.py
Paul Cobbaut, 2022-09-20 --> 2022-10-06
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
piece_length = 190               # X-coordinate in FreeCAD
piece_width = 230       # Y-coordinate in FreeCAD
piece_height = 1.5                 # Z-coordinate in FreeCAD
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

### fitting the dovetils in the pockets requires a small fitting gap
tail_fit = 0.2		# mm (makes tails a teeny bit smaller than the pockets)

### points needed for polyline sketch
# x, y
co_list = [
[0,						0						], # left_bottom
[0,						(piece_length/4) - (dove_width/2)		],
[dove_length,					(piece_length/4) - dove_width			],
[dove_length,					(piece_length/4) + dove_width			],
[0,						(piece_length/4) + (dove_width/2)		],
[0,						(piece_length*3/4) - (dove_width/2) + tail_fit	],
[0 - dove_length + tail_fit,	 		(piece_length*3/4) - dove_width + (2*tail_fit)	],
[0 - dove_length + tail_fit,	 		(piece_length*3/4) + dove_width - (2*tail_fit)	],
[0,						(piece_length*3/4) + (dove_width/2) - tail_fit	],
[0,						piece_length					], # left_top
[(piece_width/4) - (dove_width/2),		piece_length					],
[(piece_width/4) - dove_width,			piece_length - dove_length			],
[(piece_width/4) + dove_width,			piece_length - dove_length			],
[(piece_width/4) + (dove_width/2),		piece_length					],
[(piece_width*3/4) - (dove_width/2) + tail_fit,	piece_length					],
[(piece_width*3/4) - dove_width + (2*tail_fit),	piece_length + dove_length - tail_fit		],
[(piece_width*3/4) + dove_width - (2*tail_fit),	piece_length + dove_length - tail_fit		],
[(piece_width*3/4) + (dove_width/2) - tail_fit,	piece_length 					],
[piece_width,					piece_length					], # right_top
[piece_width,					(piece_length*3/4) + (dove_width/2)		],
[piece_width - dove_length,			(piece_length*3/4) + dove_width			],
[piece_width - dove_length,			(piece_length*3/4) - dove_width			],
[piece_width,					(piece_length*3/4) - (dove_width/2)		],
[piece_width,					(piece_length/4) + (dove_width/2) - tail_fit	],
[piece_width + dove_length - tail_fit,		(piece_length/4) + dove_width - (2*tail_fit)	],
[piece_width + dove_length - tail_fit,		(piece_length/4) - dove_width + (2*tail_fit)	],
[piece_width,					(piece_length/4) - (dove_width/2) + tail_fit	],
[piece_width,					0						], # right_bottom
[(piece_width*3/4) + (dove_width/2),		0						],
[(piece_width*3/4) + dove_width,		0 + dove_length					],
[(piece_width*3/4) - dove_width,		0 + dove_length					],
[(piece_width*3/4) - (dove_width/2),		0						],
[(piece_width/4) + (dove_width/2) - tail_fit,	0						],
[(piece_width/4) + dove_width - (2*tail_fit),	0 - dove_length + tail_fit			],
[(piece_width/4) - dove_width + (2*tail_fit),	0 - dove_length	+ tail_fit			],
[(piece_width/4) - (dove_width/2) + tail_fit,	0						],
[0,						0						], # left_bottom (again)
]

# create sketch using the coordinates in co_list
for i in range(len(co_list) - 1):
   sketch.addGeometry(Part.LineSegment(App.Vector(co_list[i][0], co_list[i][1], 0), App.Vector(co_list[i+1][0], co_list[i+1][1], 0)), False)


# pad this sketch
pad = doc.getObject('Body').newObject("PartDesign::Pad", "Pad")
pad.Profile = doc.getObject("Sketch")
pad.Length = piece_height

#
# we now have an empty piece with dovetails and pockets that fits with itself
#

# start putting braille on it



##braille.py
##Paul Cobbaut, 2022-07-05
##FreeCAD Braille font
##This script parses text and converts it to Braille dots in FreeCAD


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
    line_name = "line_" + str(line_count) + string
    obj = doc.addObject("Part::Compound",line_name)
    obj.Links = compound_list
    doc.recompute()	# This seems needed, otherwise nothing appears in FreeCAD

def main():
    global dot_size
    global dot_separation
    global char_separation
    global line_separation

    # line_count keeps track of the n-th line
    # is used for the position of the current line
    line_count = 0
    dot_size = .9          # diameter of a dot
    dot_separation = 2.5   # space between center of dots
    char_separation = 6.4  # space between center of characters

    create_template_dot("dot")
    print_braille_string("franse", line_count, "dot")
    line_count = line_count + 1
    print_braille_string("plaats", line_count, "dot")




main()

doc.recompute()

FreeCADGui.ActiveDocument.ActiveView.fitAll()
