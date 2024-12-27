#!/usr/bin/python3

import fileinput
from more_itertools import split_at
from P import P

def is_blank(line):
  return not(line.strip())

WALL = "#"
EMPTY = "."
BOX = "O"
LEFT = "["
RIGHT = "]"
ROBOT = "@"

BOXES = (BOX, LEFT, RIGHT)

EXPANSIONS = {
  WALL : (WALL, WALL),
  EMPTY: (EMPTY, EMPTY),
  BOX  : (LEFT, RIGHT),
  ROBOT: (ROBOT, EMPTY)
}

DIRECTIONS = {
  "<": P(-1,  0),
  ">": P( 1,  0),
  "^": P( 0, -1),
  "v": P( 0,  1)
}

UP = DIRECTIONS["^"]
DOWN = DIRECTIONS["v"]

TO_OTHER_HALF = {
  LEFT : DIRECTIONS[">"],
  RIGHT: DIRECTIONS["<"]
}

class Warehouse(dict):
  def __init__(self, lines):
    self._lines = lines
    self.init()

  def init(self, expand = False):
    for y, line in enumerate(self._lines):
      for x, char in enumerate(line.strip()):
        if expand:
          first, second = EXPANSIONS[char]
          self[P(2*x, y)] = first
          self[P(2*x + 1, y)] = second
        else:
          self[P(x, y)] = char
        if char == ROBOT:
          self.robot = P(x * (1 + expand), y)
    self.size = P((x + 1) * (1 + expand), y + 1)

  def __str__(self):
    return "\n".join("".join(self[P(x, y)] for x in range(self.size.x)) for y in range(self.size.y))

  def move(self, direction, position = None, tentative = False, is_second_half = False):
    if position == None:
      position = self.robot

    what = self[position]
    nxt = position + direction
    if what in (LEFT, RIGHT) and direction in (UP, DOWN) and not is_second_half:
      other_half = position + TO_OTHER_HALF[what]
      if not self.move(direction, other_half, tentative = True, is_second_half = True):
        return False
    else:
      other_half = None
    if (obstacle := self[nxt]) == WALL:
      return False
    elif obstacle == ROBOT:
      raise ValueError
    elif obstacle in BOXES:
      if not self.move(direction, nxt):
        return False

    # next position was (made) empty
    if not tentative:
      self[nxt] = what
      self[position] = EMPTY
      if what == ROBOT:
        self.robot = nxt
      if other_half is not None:
        self.move(direction, other_half, is_second_half = True)
    return True

  def run(self, moves, verbose = False):
    for move in moves:
      self.move(DIRECTIONS[move])

  def coordinate_sum(self):
    return sum(p.x + 100 * p.y for p, tile in self.items() if tile in (BOX, LEFT))

def read_input():
  lines, moves = split_at(fileinput.input(), is_blank)
  warehouse = Warehouse(lines)
  moves = "".join(move.strip() for move in moves)
  return warehouse, moves
    
def main():
  warehouse, moves = read_input()

  # part 1
  warehouse.run(moves)
  if warehouse.size.y < 20:
    print(warehouse)
  print(warehouse.coordinate_sum())

  # part 2
  warehouse.init(expand = True)
  warehouse.run(moves)
  if warehouse.size.y < 20:
    print(warehouse)
  print(warehouse.coordinate_sum())

if __name__ == "__main__":
  main()
