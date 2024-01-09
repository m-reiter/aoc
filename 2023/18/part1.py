#!/usr/bin/python3

import fileinput
import re

from P import P

PLAN = re.compile("([UDLR]) (\d+) \(#((\w{2})(\w{2})(\w{2}))\)")

ESC = "\033"

CUBE = "#"
EMPTY = "."

DIRECTIONS = {
  "U": P(0, -1),
  "D": P(0, 1),
  "L": P(-1, 0),
  "R": P(1, 0)
}
INT_TO_DIRECTION = "RDLU"

def rgb(text, rgb):
  return ESC+"[38;2;{};{};{}m{}".format(*rgb, text)+ESC+"[0m"

class Cube:
  def __init__(self, color = None):
    self.color = color

  def __str__(self):
    if self.color:
      return rgb(CUBE, self.color)
    return CUBE

class Dig(dict):
  def __init__(self):
    self.minx = self.maxx = self.miny = self.maxy = 0

  def __setitem__(self, key, value):
    self.minx = min(self.minx, key.x)
    self.maxx = max(self.maxx, key.x)
    self.miny = min(self.miny, key.y)
    self.maxy = max(self.maxy, key.y)

    super().__setitem__(key, value)

  def __str__(self):
    return "\n".join(
      "".join(str(self[P(x, y)]) if P(x, y) in self else EMPTY for x in self.xrange)
      for y in self.yrange
    )

  @property
  def xrange(self):
    return range(self.minx, self.maxx + 1)

  @property
  def yrange(self):
    return range(self.miny, self.maxy + 1)

  @classmethod
  def from_input(cls, corrected = False):
    dig = cls()

    position = P(0, 0)

    for line in fileinput.input():
      direction, length, hexcode, *rgb = PLAN.match(line).groups()

      if corrected:
        direction = INT_TO_DIRECTION[int(hexcode[-1])]
        length = int(hexcode[:-1], 16)
        rgb = None
      else:
        length = int(length)
        rgb = tuple(int(color, 16) for color in rgb)

      for _ in range(length):
        position += DIRECTIONS[direction]
        dig[position] = Cube(rgb)

    return dig

  def fill(self):
    for y in self.yrange:
      x = min(x for x in self.xrange if P(x, y) in self)
      if not P(x + 1, y) in self:
        break

    seeds = { P(x + 1, y) }

    while seeds:
#      print(seeds, len(self))
      seed = seeds.pop()
      seeds = seeds.union(n for n in seed.get_neighbors() if not n in self)
      self[seed] = Cube()

def main():
  dig = Dig.from_input()

  # part 1
  verbose = len(dig) < 100

  if verbose:
    print(dig)
    print()

  dig.fill()

  if verbose:
    print(dig)
    print()
  
  print(len(dig))

if __name__ == "__main__":
  main()
