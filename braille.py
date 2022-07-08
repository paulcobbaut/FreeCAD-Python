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
dotsize = 3         # diameter in mm
dotseparation = 8   # space between center of dots
charseparation = 24 # space between characters

# Number of characters that are 'printed'
charcount = 0

def make_cube(name, x, y, z):
    o = doc.addObject("Part::Box", name)
    o.Length = x
    o.Width = y
    o.Height = z
    return o


# The standard dot that is always copied
dot = doc.addObject("Part::Sphere", "dot")
dot.Radius = dotsize
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

numberindicator = "3456"

doc.recompute()

# place a dot in 1
def place_a_dot_in_1():
    global charcount
    obj = doc.addObject('Part::Feature','dot')
    obj.Shape = doc.dot.Shape
    obj.Label = "dot" + str(charcount) + "1"
    x = charcount * charseparation
    y = dotseparation * 2
    position = FreeCAD.Vector(x,y,0)
    rotation = FreeCAD.Rotation(180,0,90)
    obj.Placement = FreeCAD.Placement(position, rotation)

# place a dot in 2
def place_a_dot_in_2():
    global charcount
    obj = doc.addObject('Part::Feature','dot')
    obj.Shape = doc.dot.Shape
    obj.Label = "dot" + str(charcount) + "2"
    x = charcount * charseparation
    y = dotseparation * 1
    position = FreeCAD.Vector(x,y,0)
    rotation = FreeCAD.Rotation(180,0,90)
    obj.Placement = FreeCAD.Placement(position, rotation)


# place a dot in 3
def place_a_dot_in_3():
    global charcount
    obj = doc.addObject('Part::Feature','dot')
    obj.Shape = doc.dot.Shape
    obj.Label = "dot" + str(charcount) + "3"
    x = charcount * charseparation
    y = dotseparation * 0
    position = FreeCAD.Vector(x,y,0)
    rotation = FreeCAD.Rotation(180,0,90)
    obj.Placement = FreeCAD.Placement(position, rotation)


# place a dot in 4
def place_a_dot_in_4():
    global charcount
    obj = doc.addObject('Part::Feature','dot')
    obj.Shape = doc.dot.Shape
    obj.Label = "dot" + str(charcount) + "4"
    x = charcount * charseparation + dotseparation
    y = dotseparation * 2
    position = FreeCAD.Vector(x,y,0)
    rotation = FreeCAD.Rotation(180,0,90)
    obj.Placement = FreeCAD.Placement(position, rotation)


# place a dot in 5
def place_a_dot_in_5():
    global charcount
    obj = doc.addObject('Part::Feature','dot')
    obj.Shape = doc.dot.Shape
    obj.Label = "dot" + str(charcount) + "5"
    x = charcount * charseparation + dotseparation
    y = dotseparation * 1
    position = FreeCAD.Vector(x,y,0)
    rotation = FreeCAD.Rotation(180,0,90)
    obj.Placement = FreeCAD.Placement(position, rotation)


# place a dot in 6
def place_a_dot_in_6():
    global charcount
    obj = doc.addObject('Part::Feature','dot')
    obj.Shape = doc.dot.Shape
    obj.Label = "dot" + str(charcount) + "6"
    x = charcount * charseparation + dotseparation
    y = dotseparation * 0
    position = FreeCAD.Vector(x,y,0)
    rotation = FreeCAD.Rotation(180,0,90)
    obj.Placement = FreeCAD.Placement(position, rotation)


def print_braille_character(char):
    if "1" in braille[char]:
        place_a_dot_in_1()
    if "2" in braille[char]:
        place_a_dot_in_2()
    if "3" in braille[char]:
        place_a_dot_in_3()
    if "4" in braille[char]:
        place_a_dot_in_4()
    if "5" in braille[char]:
        place_a_dot_in_5()
    if "6" in braille[char]:
        place_a_dot_in_6()

#print_braille_character("a")

def print_braille_word(brailleword):
    previous_is_digit = False
    for letter in brailleword:
        global charcount
        if letter.isdigit():
            if previous_is_digit == False:
                previous_is_digit = True
                place_a_dot_in_3()
                place_a_dot_in_4()
                place_a_dot_in_5()
                place_a_dot_in_6()
                charcount = charcount + 1
        else:
            previous_is_digit = False
        print_braille_character(letter)
        charcount = charcount + 1


#print_braille_word("abcdefghijklmnopqrstuvwxyz1234567890")
print_braille_word("dit is braille 1 en 2 en 42")






