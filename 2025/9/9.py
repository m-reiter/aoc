#!/usr/bin/python3

import fileinput
from itertools import combinations

BOLD = '\033[1m'
END = '\033[0m'

BLANK = "."
RED = "#"
RECTANGLE = "O"
CORNER = BOLD+RECTANGLE+END


class Floor:
  def __init__(self, red_tiles):
    self.red_tiles = red_tiles
    self.width = max(r[0] for r in self.red_tiles) + 3
    self.height = max(r[1] for r in self.red_tiles) + 2
    self.corners = None

  def __str__(self):
    return "\n".join(
      "".join(self.symbol(x,y) for x in range(self.width))
      for y in range(self.height)
    )

  @staticmethod
  def area(corners):
    c1, c2 = corners
    return (abs(c1[0]-c2[0]) + 1) * (abs(c1[1]-c2[1]) + 1)

  def largest_area(self):
    return Floor.area(self.corners)

  def is_in_rectangle(self, x, y):
    left, right = sorted(c[0] for c in self.corners)
    top, bottom = sorted(c[1] for c in self.corners)

    return left <= x <= right and top <= y <= bottom

  def symbol(self, x, y):
    if self.corners:
      if (x,y) in self.corners:
        return CORNER
      elif self.is_in_rectangle(x, y):
        return RECTANGLE
    if (x,y) in self.red_tiles:
      return RED
    return BLANK

  def find_largest_rectangle(self):
    self.corners = max(((c1, c2) for c1, c2 in combinations(self.red_tiles, 2)), key = Floor.area) 

def main():
  floor = Floor([tuple(map(int, line.split(","))) for line in fileinput.input()])

  # part 1
  floor.find_largest_rectangle()
  print(floor.largest_area())

if __name__ == "__main__":
  main()
