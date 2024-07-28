#!/usr/bin/python
#make_puzzle_cubes.py -- Paul Cobbaut, 2024-07-01
#make_space_cubes.py -- Paul Cobbaut, 2024-07-27
# new version adds room so the 3D-printed can be assembled

import FreeCAD
from FreeCAD import Base, Vector
import Part
import Mesh
import random

size      = 6                                                                         # cube size
numpieces = (size * 2) + 2
full      = [[[1 for k in range(size)] for j in range(size)] for i in range(size)]    # full cube
empty     = [[[0 for k in range(size)] for j in range(size)] for i in range(size)]    # empty cube
pieces    = {}                                                                        # dict for all pieces
unitmm    = 10  # size of a 1x1x1 3D printed cube

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
        if piece != empty:
            print_cube(piecename, piece)

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

# moves one cubeunit from fromcube to tocube
def move(fromcube, tocube, x, y, z):
    if fromcube[x][y][z] == 1 and tocube[x][y][z] == 0:
        fromcube[x][y][z] = 0
        tocube[x][y][z] = 1
    else:
        print("Error PC: problem in move")
        quit()


def make_piece_x(piece):
    # choose a random coordinate on this side
    Y = random.randint(0, size - 1)
    Z = random.randint(0, size - 1)
    # remove longest length piece at coordinate
    x = 0
    if full[x][Y][Z] == 1:
        move(full, piece, x, Y, Z)
        for other_x in range(size - 1):
            if full[x + other_x + 1][Y][Z] == 0:
                return
            elif full[x + other_x + 1][Y][Z] == 1:
                move(full, piece, x + other_x + 1, Y, Z)


def make_piece_y(piece):
    # choose a random coordinate on this side
    X = random.randint(0, size - 1)
    Z = random.randint(0, size - 1)
    # remove longest length piece at coordinate
    y = 0
    if full[X][y][Z] == 1:
        move(full, piece, X, y, Z)
        for other_y in range(size - 1):
            if full[X][y + other_y + 1][Z] == 0:
                return
            elif full[X][y + other_y + 1][Z] == 1:
                move(full, piece, X, y + other_y + 1, Z)


def make_piece_z(piece):
    # choose a random coordinate on this side
    X = random.randint(0, size - 1)
    Y = random.randint(0, size - 1)
    # remove longest length piece at coordinate
    z = 0
    if full[X][Y][z] == 1:
        move(full, piece, X, Y, z)
        for other_z in range(size - 1):
            if full[X][Y][z + other_z + 1] == 0:
                return
            elif full[X][Y][z + other_z + 1] == 1:
                move(full, piece, X, Y, z + other_z + 1)


# for numpieces
for i in range(numpieces):
    currentpiece = "piece{0}".format(i)
    pieces[currentpiece] = [[[0 for kk in range(size)] for jj in range(size)] for ii in range(size)]
    ## random x,y or z
    ## create longest possible piece
    choice = random.choice(["x", "y", "z"])
    if choice == "x":
        while pieces[currentpiece] == empty:
            make_piece_x(pieces[currentpiece])
    if choice == "y":
        while pieces[currentpiece] == empty:
            make_piece_y(pieces[currentpiece])
    if choice == "z":
        while pieces[currentpiece] == empty:
            make_piece_z(pieces[currentpiece])

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
                    if Z == 1:
                        piecepart = makeunitcube(x,y,z)
                        compound_piece.append(piecepart)
        make_3mf(piecename, compound_piece)


#print_all_pieces()
pieces_to_3mf(pieces)


'''
def move_row(fromcube, pieceindex, x, y):
    for z in range(size):
        move(fromcube, pieces["blk{0}".format(pieceindex)], x, y, z)

def move_unit(fromcube, pieceindex, x, y, z):
        move(fromcube, pieces["blk{0}".format(pieceindex)], x, y, z)



def unit_still_in_full(x, y, z):
    if full[x][y][z] == 1:
        return True
    return False

def move_unit_to_adjacent(x, y, z):
    # find current adjacent pieces
    adj = []
    for piecename, piece in pieces.items():
        if x >= 1:
            tx = x - 1
        else:
            tx = x
        if piece[tx][y][z] == 1:
            adj.append(piecename)
        if x == size - 1:
            tx = x
        else:
            tx = x + 1
        if piece[tx][y][z] == 1:
            adj.append(piecename)
        if y >= 1:
            ty = y - 1
        else:
            ty = y
        if piece[x][ty][z] == 1:
            adj.append(piecename)
        if y == size - 1:
            ty = y
        else:
            ty = y + 1
        if piece[x][ty][z] == 1:
            adj.append(piecename)
    print('adjacent are ' + str(adj))
    # choose one of the adjacent pieces and attach to it
    move_unit(full, random.choice(adj)[3:], x, y, z)
    return

# creates straight pieces but skips one every time
skip = True
i = 0
for x in range(size):
    for y in range(size):
        pieces["blk{0}".format(i)] = [[[0 for k in range(size)] for j in range(size)] for i in range(size)]
        if skip:
            move_row(full, i, x, y)
            skip = False
        else:
            skip = True
        i += 1

# second round
for x in range(size):
    for y in range(size):
        for z in range(size):
            if unit_still_in_full(x,y,z):
                move_unit_to_adjacent(x,y,z)

#print_all_pieces()
'''
