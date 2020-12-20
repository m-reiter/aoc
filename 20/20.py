#!/usr/bin/python3

import fileinput
from more_itertools import split_at
from math import sqrt
from collections import defaultdict
from functools import reduce
from operator import mul
import re

MONSTER = """                  # 
#    ##    ##    ###
 #  #  #  #  #  #   """

class Tile:

  def __init__(self, lines):

    self.orientation = 0
    
    self.number = lines[0].strip().split()[1].rstrip(":")

    self.grid = [line.strip() for line in lines[1:]]

    self.dim = len(self.grid)

    top = self.grid[0]
    bottom = self.grid[-1]
    left = "".join(self.grid[i][0] for i in range(self.dim))
    right = "".join(self.grid[i][-1] for i in range(self.dim))

    self.tops = [ top, left[::-1], bottom[::-1], right, top[::-1], right[::-1], bottom, left ]
    self.bottoms = [ bottom, right[::-1], top[::-1], left, bottom[::-1], left[::-1], top, right ]
    self.lefts = [ left, bottom, right[::-1], top[::-1], right, bottom[::-1], left[::-1], top ]
    self.rights = [ right, top, left[::-1], bottom[::-1], left, top[::-1], right[::-1], bottom ]

  def flip(self):

    self.orientation = (self.orientation+4) % 7

    self.grid = [line[::-1] for line in self.grid]

  def rotate(self):

    self.orientation += 1

    self.grid = ["".join(self.grid[y][x] for y in range(self.dim))[::-1] for x in range(self.dim)]

  def strip(self):

    self.grid = [line[1:-1] for line in self.grid[1:-1]]
    self.dim -= 2

  def find(self, pattern):

    length = len(pattern.split("\n")[0])
    height = len(pattern.split("\n"))

    pattern_re = re.compile(pattern.replace(" ","."))

    found = 0

    while found == 0:

      for i in range(self.dim - length):

        found += len(pattern_re.findall("\n".join(line[i:i+length] for line in self.grid)))

      self.rotate()

      if self.orientation == 4:
        self.flip()

    return found


class Grid:

  def __init__(self, dim):

    self.dim = dim

    self.left = defaultdict(lambda: defaultdict(lambda: None))
    self.top = defaultdict(lambda: defaultdict(lambda: None))
    self.tiles = [[None]*dim for i in range(dim)] 
    self.orientations = [[None]*dim for i in range(dim)] 

  def place(self, x, y, tile, orientation):

    self.left[y][x+1] = tile.rights[orientation]
    self.top[y+1][x] = tile.bottoms[orientation]
    self.tiles[y][x] = int(tile.number)
    self.orientations[y][x] = orientation

  def remove(self, x, y):

    self.left[y][x+1] = None
    self.top[y+1][x] = None
    self.tiles[y][x] = None

  def solve(self,tiles, x=0, y=0):

    if len(tiles) == 0:
    
      return self
      
    left = self.left[y][x]
    top = self.top[y][x]
    
    xnew = (x+1) % self.dim
    ynew = y if xnew else (y+1) % self.dim

    for tile in tiles:

      if left == None:

        for orientation in range(len(tile.lefts)):
        #for orientation in (0,4):

          self.place(x,y,tile,orientation)

          newtiles = tiles.copy()
          newtiles.remove(tile)

          if self.solve(newtiles,xnew,ynew):

            return self

          self.remove(x,y)

      elif not left in tile.lefts:
        
        next

      for orientation, tile_left in enumerate(tile.lefts):

        if left == tile_left and (top == None or top == tile.tops[orientation]):

          self.place(x,y,tile,orientation)

          newtiles = tiles.copy()
          newtiles.remove(tile)
          
          if self.solve(newtiles,xnew,ynew):

            return self

    return False

  def corners(self):

    return (self.tiles[0][0], self.tiles[0][-1], self.tiles[-1][0], self.tiles[-1][-1])

  def assemble(self, tiles):

    tiles_dict = {int(tile.number): tile for tile in tiles}

    for y in range(self.dim):
      for x in range(self.dim):

        tiles_dict[self.tiles[y][x]].strip()
        
        if self.orientations[y][x] > 3:
          tiles_dict[self.tiles[y][x]].flip()
          self.orientations[y][x] -= 4

        for i in range(self.orientations[y][x]):
          tiles_dict[self.tiles[y][x]].rotate()

    image = []
    tiledim = tiles[0].dim

    for y in range(self.dim):

      image += ["".join(tiles_dict[self.tiles[y][x]].grid[i] for x in range(self.dim)) for i in range(tiledim)]

    return Tile(["dummy image"]+image)

def main():
  
  tiles = [Tile(t) for t in split_at(fileinput.input(), lambda x: not x.strip())]

  grid_dim = int(sqrt(len(tiles)))

  grid = Grid(grid_dim)

  solution = grid.solve(tiles)

  if solution:
    print(reduce(mul,solution.corners(),1))

  image = solution.assemble(tiles)

  monsters = image.find(MONSTER)

  roughness = "".join(image.grid).count("#") - monsters * MONSTER.count("#")

  print(roughness)

if __name__ == "__main__":
  main()
