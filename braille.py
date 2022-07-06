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
  "d" : "145"
}


doc.recompute()

# place a dot in 1
def place_a_dot():
    obj = doc.addObject('Part::Feature','dot')
    obj.Shape = doc.dot.Shape
    obj.Placement = FreeCAD.Placement(Vector(0, 0, 0), FreeCAD.Rotation(180,0,90), Vector(0,0,0))

# place a dot in 2
def place_a_dot_in_2():
    obj = doc.addObject('Part::Feature','dot')
    obj.Shape = doc.dot.Shape
    position = FreeCAD.Vector(50,0,0)
    rotation = FreeCAD.Rotation(180,0,90)
    obj.Placement = FreeCAD.Placement(position, rotation)


def print_braille_character(char):
    if "1" in braille[char]:
        print("1 erin")
    if "2" in braille[char]:
        print("2 erin")
        place_a_dot_in_2()
    if "3" in braille[char]:
        print("3 erin")
    if "4" in braille[char]:
        print("4 erin")
    if "5" in braille[char]:
        print("5 erin")
        place_a_dot()
    if "6" in braille[char]:
        print("6 erin")

print("test a")
print_braille_character("a")

print("test b")
print_braille_character("b")

print("test d")
print_braille_character("d")







