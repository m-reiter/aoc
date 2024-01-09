#!/usr/bin/python3

import fileinput

from itertools import combinations

from P import P

GALAXY = "#"

class Map:
  def __init__(self):
    self.dimx = 0
    self.dimy = 0
    self.galaxies = []
    self.corrected = None
    self.empty_rows = []
    self.empty_columns = []

  def add_galaxy(self, x, y):
    self.dimx = max(x, self.dimx)
    self.dimy = max(y, self.dimy)
    self.galaxies.append(P(x, y))

  @classmethod
  def from_fileinput(cls):
    newmap = cls()
    for y,line in enumerate(fileinput.input()):
      for x,char in enumerate(line):
        if char == GALAXY:
          newmap.add_galaxy(x, y)
    return newmap

  def expand(self, age = 2):
    self.empty_rows = [ y for y in range(self.dimy) if not any(galaxy.y == y for galaxy in self.galaxies) ]
    self.empty_columns = [ x for x in range(self.dimx) if not any(galaxy.x == x for galaxy in self.galaxies) ]

    self.corrected = [
      P(
        x + (age - 1) * sum(x > column for column in self.empty_columns),
        y + (age - 1) * sum(y > row for row in self.empty_rows)
      ) for x,y in self.galaxies
    ]

def main():
  cosmos = Map.from_fileinput()

  # part 1
  cosmos.expand()

  print(sum(sum(map(abs, (a-b))) for a,b in combinations(cosmos.corrected, 2)))

  # part 2
  cosmos.expand(1000000)

  print(sum(sum(map(abs, (a-b))) for a,b in combinations(cosmos.corrected, 2)))

if __name__ == "__main__":
  main()
