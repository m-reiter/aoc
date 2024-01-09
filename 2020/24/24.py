#!/usr/bin/python3

import fileinput
from collections import defaultdict
import re

class P(tuple):

  def __add__(self, other):

    return P(x1+x2 for x1,x2 in zip(self, other))

  def __mul__(self, integer):

    return P(x * integer for x in self)

  @property
  def x(self):

    return self[0]

  @property
  def y(self):

    return self[1]

  __rmul__ = __mul__

NEIGHBORS = {
  'nw': P(( 0,-1)),
  'ne': P(( 1,-1)),
  'w_': P((-1, 0)),
  'e_': P(( 1, 0)),
  'sw': P((-1, 1)),
  'se': P(( 0, 1))
}

class Tiles:

  def __init__(self):

    self.tiles = defaultdict(bool)

    self.day = 0

  def __getitem__(self, point):

    return self.tiles[point]

  def __setitem__(self, point, value):

    self.tiles[point] = value

  def parseline(self, line):

    line = re.sub(r"(?<![ns])([we])", r"\1_", line)

    target = P((0,0))

    for direction, value in NEIGHBORS.items():

      target += line.count(direction) * value

    self[target] = not self[target]

  def count_blacks(self):

    return sum(x for x in self.tiles.values())

  def pass_day(self, verbose = False):

    self.day += 1

    neighbor_count = defaultdict(int)

    for point in self.tiles:

      if self[point]:

        for neighbor in NEIGHBORS.values():

          neighbor_count[point + neighbor] += 1

    for black in [x for x in self.tiles if self[x]]:

      if not 0 < neighbor_count[black] <= 2:

        self[black] = False

    for white in [x for x,y in neighbor_count.items() if y == 2 and not self[x]]:

      self[white] = True

    if verbose and self.day < 10 or self.day % 10 == 0:

      print("Day {}: {}".format(self.day, self.count_blacks()))

      if self.day == 10: print()
    

def main():
  
  tiles = Tiles()

  for line in fileinput.input():

    tiles.parseline(line.strip())

  print(tiles.count_blacks())

  for i in range(100):

    tiles.pass_day(verbose = True)

if __name__ == "__main__":
  main()
