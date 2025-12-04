#!/usr/bin/python3

import fileinput

from P import P

PAPER_ROLL = "@"
EMPTY = "."

class Grid(dict):
  def __init__(self, diagram):
    for y, line in enumerate(diagram):
      for x, character in enumerate(line):
        if character == PAPER_ROLL:
          self[P(x,y)] = PAPER_ROLL

    self.size = P(x+1,y+1)

  def __str__(self):
    return "\n".join(
      "".join(EMPTY if self.is_empty(P(x,y)) else PAPER_ROLL for x in range(self.size.x))
      for y in range(self.size.y)
    )

  def show_accessibles(self):
    return "\n".join(
      "".join(EMPTY if self.is_empty(P(x,y)) else "x" if self.is_accessible(P(x,y)) else PAPER_ROLL for x in range(self.size.x))
      for y in range(self.size.y)
    )

  def is_empty(self, position):
    return self.get(position, None) is None

  def is_roll(self, position):
    return position in self.keys()

  def is_accessible(self, position):
    if not self.is_roll(position):
      return False
    return sum(self.is_roll(n) for n in position.get_neighbors(borders = self.size-P(1,1))) < 4

  def count_accessibles(self):
    return sum(self.is_accessible(roll) for roll in self.keys())

def main():
  grid = Grid(fileinput.input())
  
  # part 1
  print(grid.count_accessibles())

if __name__ == "__main__":
  main()
