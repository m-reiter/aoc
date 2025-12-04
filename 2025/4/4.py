#!/usr/bin/python3

import fileinput

from P import P

PAPER_ROLL = "@"
EMPTY = "."
ACCESSIBLE = "x"

class Grid(set):
  def __init__(self, diagram):
    for y, line in enumerate(diagram):
      for x, character in enumerate(line):
        if character == PAPER_ROLL:
          self.add(P(x,y))

    self.size = P(x+1,y+1)

  def __str__(self):
    return self.pretty(show_accessibles = False)

  def pretty(self, show_accessibles = True):
    accessibles = self.get_accessibles()
    return "\n".join(
      "".join(
        ACCESSIBLE if show_accessibles and P(x,y) in accessibles
        else PAPER_ROLL if self.is_roll(P(x,y))
        else EMPTY
        for x in range(self.size.x)
      )
      for y in range(self.size.y)
    )

  def is_roll(self, position):
    return position in self

  def is_accessible(self, position):
    return self.is_roll(position) and sum(self.is_roll(n) for n in position.get_neighbors(borders = self.size-P(1,1))) < 4

  def get_accessibles(self):
    return [ roll for roll in self if self.is_accessible(roll) ]

  def count_accessibles(self):
    return len(self.get_accessibles())

  def remove_rolls(self, positions):
    for p in positions:
      self.remove(p)

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

  while (n := len(removables := grid.get_accessibles()))  > 0:
    if verbose:
      print(f"Remove {n} roll{'s' if n > 1 else ''} of paper:")
      print(grid.pretty())
      print()
    grid.remove_rolls(removables)
    removed += len(removables)

  if verbose:
    print("Final state:")
    print(grid)
    print()

  print(removed)

if __name__ == "__main__":
  main()
