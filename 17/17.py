#!/usr/bin/python3

import fileinput
from collections import defaultdict

class P(tuple):

  def __add__(self, other):

    return P(x1+x2 for x1,x2 in zip(self, other))

NEIGHBORS3D = [P((x,y,z)) for x in range(-1,2) for y in range(-1,2) for z in range(-1,2) if x or y or z]
NEIGHBORS4D = [P((x,y,z,w)) for x in range(-1,2) for y in range(-1,2) for z in range(-1,2) for w in range(-1,2) if x or y or z or w]

class PocketDimension:

  def __init__(self, input_):

    self.dimensions = 3
    self.neighbors = NEIGHBORS3D
    self.active_cubes = []
    self.cycle = 0
    
    y = 0
    for line in input_:
      for x, cube in enumerate(line):
        if cube == "#":
          self.active_cubes.append(P((x, y, 0)))
      y += 1

  def __str__(self):

    str_ = "cycle: {}\n".format(self.cycle)

    xrange, yrange, zrange = self.bounding_box

    for z in range(*zrange):

      str_ += "\nz={}\n".format(z)

      for y in range(*yrange):
        for x in range(*xrange):
          if (x,y,z) in self.active_cubes:
            str_ += "#"
          else:
            str_ += "."
        str_ += "\n"

    return str_

  @property
  def bounding_box(self):

    return [P((min(cube[i] for cube in self.active_cubes), max(cube[i] for cube in self.active_cubes) + 1)) for i in range(self.dimensions)]

  def step(self, verbose = True):

    next_cubes = []
    occupied_neighbors = defaultdict(int)

    for cube in self.active_cubes:
      for neighbor in self.neighbors:
        occupied_neighbors[cube+neighbor] += 1

    for cube,n in occupied_neighbors.items():
      if n == 3 or n == 2 and cube in self.active_cubes:
        next_cubes.append(cube)

    self.cycle += 1

    self.active_cubes = next_cubes

    if verbose:
      print(self)

class PocketDimension4D(PocketDimension):

  def __init__(self, input_):

    super().__init__(input_)

    self.dimensions = 4
    self.neighbors = NEIGHBORS4D

    self.active_cubes = [P(tuple(cube)+(0,)) for cube in self.active_cubes]

  def __str__(self):

    str_ = "cycle: {}\n".format(self.cycle)

    xrange, yrange, zrange, wrange = self.bounding_box

    for w in range(*wrange):
      for z in range(*zrange):

        str_ += "\nz={}, w={}\n".format(z,w)

        for y in range(*yrange):
          for x in range(*xrange):
            if (x,y,z,w) in self.active_cubes:
              str_ += "#"
            else:
              str_ += "."
          str_ += "\n"

    return str_

    

def main():
  
  input_ = list(fileinput.input())

  pd = PocketDimension(input_)

  while pd.cycle < 6:
    pd.step()

  sol1 = len(pd.active_cubes)

  pd = PocketDimension4D(input_)

  while pd.cycle < 6:
    pd.step()

  sol2 = len(pd.active_cubes)

  print("solution part 1: {}".format(sol1))
  print("solution part 2: {}".format(sol2))

if __name__ == "__main__":
  main()
