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


def make_cube(name, x, y, z):
    o = doc.addObject("Part::Box", name)
    o.Length = x
    o.Width = y
    o.Height = z
    return o


# make base (resembling A4) to put demo font on
paper = make_cube("paper", 297, 210, 1)


dot = doc.addObject("Part::Sphere", "dot")
dot.Radius = 20
dot.Angle1 = -90
dot.Angle2 = 90
dot.Angle3 = 180
dot.Placement = FreeCAD.Placement(Vector(0, 0, 0), FreeCAD.Rotation(180, 0, 90))
dot.ViewObject.hide()

# positions of braille dots
14
25
36

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
"""

braille = {
  "a" : "1",
  "b" : "12",
  "c" : "14",
  "d" : "145",
  "e" : "15"
}


doc.recompute()

# place a dot in 1
def place_a_dot_in_1():
    obj = doc.addObject('Part::Feature','dot')
    obj.Shape = doc.dot.Shape
    obj.Label = "dot1"
    position = FreeCAD.Vector(0,100,0)
    rotation = FreeCAD.Rotation(180,0,90)
    obj.Placement = FreeCAD.Placement(position, rotation)

# place a dot in 2
def place_a_dot_in_2():
    obj = doc.addObject('Part::Feature','dot')
    obj.Shape = doc.dot.Shape
    obj.Label = "dot2"
    position = FreeCAD.Vector(0,50,0)
    rotation = FreeCAD.Rotation(180,0,90)
    obj.Placement = FreeCAD.Placement(position, rotation)


# place a dot in 3
def place_a_dot_in_3():
    obj = doc.addObject('Part::Feature','dot')
    obj.Shape = doc.dot.Shape
    obj.Label = "dot3"
    position = FreeCAD.Vector(0,0,0)
    rotation = FreeCAD.Rotation(180,0,90)
    obj.Placement = FreeCAD.Placement(position, rotation)


# place a dot in 4
def place_a_dot_in_4():
    obj = doc.addObject('Part::Feature','dot')
    obj.Shape = doc.dot.Shape
    obj.Label = "dot4"
    position = FreeCAD.Vector(50,100,0)
    rotation = FreeCAD.Rotation(180,0,90)
    obj.Placement = FreeCAD.Placement(position, rotation)


# place a dot in 5
def place_a_dot_in_5():
    obj = doc.addObject('Part::Feature','dot')
    obj.Shape = doc.dot.Shape
    obj.Label = "dot5"
    position = FreeCAD.Vector(50,50,0)
    rotation = FreeCAD.Rotation(180,0,90)
    obj.Placement = FreeCAD.Placement(position, rotation)


# place a dot in 6
def place_a_dot_in_6():
    obj = doc.addObject('Part::Feature','dot')
    obj.Shape = doc.dot.Shape
    obj.Label = "dot6"
    position = FreeCAD.Vector(50,0,0)
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

#print("test a")
#print_braille_character("a")

#print("test b")
#print_braille_character("b")

print("test d")
print_braille_character("d")







