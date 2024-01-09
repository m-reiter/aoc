#!/usr/bin/python3

import fileinput
import re

from collections import defaultdict

from P import P

ON = re.compile("#")
STEPS = 100
#STEPS = 5

class Grid(defaultdict):
  def __init__(self, dimensions = P(0,0)):
    super().__init__(int)
    self.dimensions = dimensions

  def __str__(self):
    return "\n".join("".join("#" if self[P(x,y)] else "." for x in range(self.dimensions.x)) for y in range(self.dimensions.y))

  def light_corners(self):
    for x in 0, self.dimensions.x - 1:
      for y in 0, self.dimensions.y - 1:
        self[P(x,y)] = 1

def read_input():
  grid = Grid()

  for y, line in enumerate(fileinput.input()):
    dimx = len(line.strip())
    for x in [ l.start() for l in ON.finditer(line) ]:
      grid[P(x,y)] = 1

  grid.dimensions = P(dimx, y + 1)

  return grid

def evolve(grid):
  new = Grid(grid.dimensions)

  for x in range(grid.dimensions.x):
    for y in range(grid.dimensions.y):
      neighbors = sum(grid[p] for p in P(x,y).get_neighbors())
      if neighbors == 3 or (grid[P(x,y)] and neighbors == 2):
        new[P(x,y)] = 1

  return new

def main():
  grid = read_input()

  # part 1
  current = Grid(grid.dimensions)
  current.update(grid)
  for _ in range(STEPS):
    current = evolve(current)

  print(sum(current.values()))

  # part 2
  grid.light_corners()
  print(grid)
  for _ in range(STEPS):
    grid = evolve(grid)
    grid.light_corners()

  print(sum(grid.values()))

if __name__ == "__main__":
  main()
