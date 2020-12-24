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

    self.tiles = defaultdict(lambda: defaultdict(bool))

  def __getitem__(self, point):

    return self.tiles[point.x][point.y]

  def __setitem__(self, point, value):

    self.tiles[point.x][point.y] = value

  def parseline(self, line):

    line = re.sub(r"(?<![ns])([we])", r"\1_", line)

    target = P((0,0))

    for direction, value in NEIGHBORS.items():

      target += line.count(direction) * value

    self[target] = not self[target]

  def count_blacks(self):

    return sum(sum(x.values()) for x in self.tiles.values())

def main():
  
  tiles = Tiles()

  for line in fileinput.input():

    tiles.parseline(line.strip())

  print(tiles.count_blacks())

if __name__ == "__main__":
  main()
