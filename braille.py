"""
braille.py
Paul Cobbaut, 2022-07-05
Attempting to create FreeCAD Braille font
"""

import FreeCAD
from FreeCAD import Base, Vector
import Part

# FreeCAD document
doc = FreeCAD.newDocument("Braille demo")


# Font size
dot_size = 3         # diameter in mm
dot_separation = 8   # space between center of dots
char_separation = 24 # space between characters
line_separation = 32 # space between lines

# Number of characters that are 'printed' on a single line
char_count = 0
line_count = 0

# This is the standard dot that is always copied
dot = doc.addObject("Part::Sphere", "dot")
dot.Radius = dot_size
dot.Angle1 = -90
dot.Angle2 = 90
dot.Angle3 = 180
dot.Placement = FreeCAD.Placement(Vector(0, 0, 0), FreeCAD.Rotation(180, 0, 90))
dot.ViewObject.hide()


# positions of braille dots
"""
14
25
36
"""


# braille alphabet
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

# This seems needed, otherwise nothing appears in FreeCAD
doc.recompute()


# place a dot in the correct position
def place_a_dot(dot_number):					# dot_number is Braille dot 1, 2, 3, 4, 5 or 6
    global char_count						# so we can move further one char_separation for each character
    obj = doc.addObject('Part::Feature','dot')			# copy the template dot
    obj.Shape = doc.dot.Shape
    obj.Label = "dot" + str(char_count) + str(dot_number)	# name has 'some' meaning: dot + character position + Braille dot
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


# prints one Braille character
def print_braille_character(char):
    if "1" in braille[char]:
        place_a_dot(1)
    if "2" in braille[char]:
        place_a_dot(2)
    if "3" in braille[char]:
        place_a_dot(3)
    if "4" in braille[char]:
        place_a_dot(4)
    if "5" in braille[char]:
        place_a_dot(5)
    if "6" in braille[char]:
        place_a_dot(6)


# prints one Braille string
def print_braille_string(string):
    previous_is_digit = False
    for letter in string:
        global char_count
        char_count = char_count + 1
        if letter.isdigit():
            if previous_is_digit == False:
                previous_is_digit = True
                # Braille Number Indicator = "3456"
                place_a_dot(3)
                place_a_dot(4)
                place_a_dot(5)
                place_a_dot(6)
                char_count = char_count + 1
        else:
            previous_is_digit = False
        print_braille_character(letter)
    global line_count
    line_count = line_count + 1
    char_count = 0


print_braille_string("abcdefghijklmnopqrstuvwxyz  1234567890")
print_braille_string("dit is braille 1 en 2 en 42")
print_braille_string("alea jacta est")
print_braille_string("2 4 8 16 32 64 128 256")


