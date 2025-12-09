#!/usr/bin/python3

import fileinput
from itertools import combinations, pairwise
from enum import Enum, auto

BOLD = '\033[1m'
END = '\033[0m'

RED = "#"
GREEN = "X"
UNKNOWN = "."
RECTANGLE = "O"
CORNER = BOLD+RECTANGLE+END

class State(Enum):
  OUTSIDE = auto()
  ENTERING = auto()
  INSIDE = auto()
  EXITING = auto()

class Floor:
  def __init__(self, red_tiles):
    self.red_tiles = red_tiles
    self.green_tiles = set()
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
  
  @staticmethod
  def connection(c1, c2):
    if c1[0] == c2[0]: # vertical line
      top, bottom = sorted((c1[1], c2[1]))
      return { (c1[0], y) for y in range((top + 1), bottom) }
    assert c1[1] == c2[1] # no diagonal lines
    left, right = sorted((c1[0], c2[0]))
    return { (x, c1[1]) for x in range((left + 1), right) }

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
    if self.green_tiles and (x,y) in self.green_tiles:
      return GREEN
    return UNKNOWN

  def only_red_or_green(self, c1, c2):
    left, right = sorted((c1[0], c2[0]))
    top, bottom = sorted((c1[1], c2[1]))
    for x in range(left, right + 1):
      for y in range(top, bottom + 1):
        if not ((x,y) in self.red_tiles or (x,y) in self.green_tiles):
          return False
    return True

  def find_largest_rectangle(self, only_red_or_green = False):
    if only_red_or_green:
      condition = self.only_red_or_green
    else:
      condition = lambda x1, x2: True
    self.corners = max(((c1, c2) for c1, c2 in combinations(self.red_tiles, 2) if condition(c1, c2)), key = Floor.area) 

  def find_green_borders(self):
    self.corners = None
    for r1, r2 in pairwise(self.red_tiles + [ self.red_tiles[0] ]):
      self.green_tiles |= Floor.connection(r1, r2)
    
  def fill_green_tiles(self):
    for y in range(self.height - 1):
      state = State.OUTSIDE
      for x in range(self.width - 2):
        if state == State.OUTSIDE:
          if (x, y) in self.red_tiles or (x, y) in self.green_tiles:
            state = State.ENTERING
        elif state == State.ENTERING:
          if not (x, y) in self.red_tiles and not (x, y) in self.green_tiles:
            state = state.INSIDE
        elif state == State.EXITING:
          if not (x, y) in self.red_tiles and not (x, y) in self.green_tiles:
            state = State.OUTSIDE
        if state == State.INSIDE: # could be just set
          if (x, y) in self.red_tiles or (x, y) in self.green_tiles:
            state == State.EXITING
          else:
            self.green_tiles.add((x, y))

def main():
  floor = Floor([tuple(map(int, line.split(","))) for line in fileinput.input()])

  verbose = len(floor.red_tiles) < 10
  if verbose:
    print("Initial state:")
    print(floor)
    print()

  # part 1
  floor.find_largest_rectangle()
  if verbose:
    print("Largest rectangle without regarding green tiles:")
    print(floor)
    print()
  print(f"Area: {floor.largest_area()}")

  # part 2
  floor.find_green_borders()
  if verbose:
    print()
    print("Green borders added:")
    print(floor)
    print()

  floor.fill_green_tiles()
  if verbose:
    print()
    print("All green tiles filled in:")
    print(floor)
    print()

  floor.find_largest_rectangle(only_red_or_green = True)
  if verbose:
    print("Largest rectangle with regarding green tiles:")
    print(floor)
    print()
  print(f"Area: {floor.largest_area()}")

if __name__ == "__main__":
  main()
