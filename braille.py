"""
braille.py
Paul Cobbaut, 2022-07-05
FreeCAD Braille font
This script parses text and converts it to Braille dots in FreeCAD
"""

import FreeCAD
from FreeCAD import Base, Vector
import Part

# FreeCAD document
doc = FreeCAD.newDocument("Braille demo")

# These four define the size of the dots in mmm
dot_size = 3         # diameter of a dot
dot_separation = 8   # space between center of dots
char_separation = 24 # space between center of characters
line_separation = 32 # space between center of lines


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
    line_name = "line_" + str(line_count)
    obj = doc.addObject("Part::Compound",line_name)
    obj.Links = compound_list
    doc.recompute()	# This seems needed, otherwise nothing appears in FreeCAD


# program starts here
def main():
    create_template_dot()
    # line_count keeps track of the n-th line
    # is used for the position of the current line
    line_count = 0

    #print_braille_string("abcdefghijklmnopqrstuvwxyz", line_count)
    #line_count = line_count + 1
    #print_braille_string("abcdefghijklmnopqrstuvwxyz", line_count)
    #line_count = line_count + 1
    print_braille_string("-1  sport", line_count)
    line_count = line_count + 1
    print_braille_string("vuil atelier", line_count)
    line_count = line_count + 1
   

main()

