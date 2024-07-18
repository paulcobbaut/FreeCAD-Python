#!/usr/bin/python
#make_puzzle_cubes.py -- Paul Cobbaut, 2024-07-01
#the part of the code without FreeCAD

import FreeCAD
from FreeCAD import Base, Vector
import Part
import Mesh

size   = 3                                                                         # cube size
full   = [[[1 for k in range(size)] for j in range(size)] for i in range(size)]    # full cube
empty  = [[[0 for k in range(size)] for j in range(size)] for i in range(size)]    # empty cube
pieces = {}                                                                        # dict for all pieces

unitmm = 10  # size of a 1x1x1 3D printed cube

# FreeCAD document
doc = FreeCAD.newDocument("Puzzel")

def print_cube(cubename, cube):
    print("Cube start: " + cubename)
    for i in cube:
        print('[')
        for j in i:
            print(' [', end='')
            for k in j:
                print(k, end='')
            print(']')
        print(']')
    print("Cube end: " + cubename)

def print_all_pieces():
    for piecename, piece in pieces.items():
        print_cube(piecename, piece)

def move(fromcube, tocube, x, y, z):
    if fromcube[x][y][z] == 1 and tocube[x][y][z] == 0:
        fromcube[x][y][z] = 0
        tocube[x][y][z] = 1
    else:
        print("Error PC: problem in move")
        quit()

def move_row(fromcube, pieceindex, x, y):
    for z in range(size):
        move(fromcube, pieces["blk{0}".format(pieceindex)], x, y, z)

def makeunitcube(x, y, z):
    obj        = doc.addObject("Part::Box","Box")
    obj.Label  = "Box"
    obj.Length = unitmm
    obj.Width  = unitmm
    obj.Height = unitmm
    position = FreeCAD.Vector(unitmm*x, unitmm*y, unitmm*z)
    obj.Placement = FreeCAD.Placement(position, FreeCAD.Rotation(Vector(0,0,1),0))
    doc.recompute()
    return obj

def make_3mf(name, compound):
    cobj = doc.addObject("Part::Compound", name)
    cobj.Links = compound
    doc.recompute()
    export_list = []
    export_list.append(cobj)
    Mesh.export(export_list, u"/home/paul/FreeCAD_generated/" + name + ".stl")

def pieces_to_3mf(pieces):
    for piecename, piece in pieces.items():
        compound_piece = []
        for x, X in enumerate(piece):
            for y, Y in enumerate(X):
                for z, Z in enumerate(Y):
                    print(Z)
                    if Z == 1:
                        piecepart = makeunitcube(x,y,z)
                        compound_piece.append(piecepart)
        make_3mf(piecename, compound_piece)


# creates straight pieces to fill the cube
i = 0
for x in range(size):
    for y in range(size):
        pieces["blk{0}".format(i)] = [[[0 for k in range(size)] for j in range(size)] for i in range(size)]
        move_row(full, i, x, y)
        i += 1

'''
# creates straight pieces but skips one every time
i = 0
for x in range(size):
    for y in range(size):
        pieces["blk{0}".format(i)] = [[[0 for k in range(size)] for j in range(size)] for i in range(size)]
        move_row(full, i, x, y)
        i += 1
'''

print_all_pieces()
pieces_to_3mf(pieces)


