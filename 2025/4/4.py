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
    accessibles = self.get_accessibles()
    return "\n".join(
      "".join(EMPTY if self.is_empty(P(x,y)) else "x" if P(x,y) in accessibles else PAPER_ROLL for x in range(self.size.x))
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

  def get_accessibles(self):
    return [ roll for roll in self.keys() if self.is_accessible(roll) ]

  def count_accessibles(self):
    return len(self.get_accessibles())

  def remove(self, positions):
    for p in positions:
      del self[p]

def main():
  grid = Grid(fileinput.input())
  
  # part 1
  print(grid.count_accessibles())

  # part 2
  verbose = grid.size.x < 20

  if verbose:
    print()
    print("Initial state:")
    print(grid)
    print()

  removed = 0

  while len(removables := grid.get_accessibles())  > 0:
    if verbose:
      print(f"Remove {len(removables)} rolls of paper:")
      print(grid.show_accessibles())
      print()
    grid.remove(removables)
    removed += len(removables)

  if verbose:
    print("Final state:")
    print(grid)
    print()

  print(removed)

if __name__ == "__main__":
  main()
