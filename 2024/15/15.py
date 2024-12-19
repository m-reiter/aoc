#!/usr/bin/python3

import fileinput
from more_itertools import split_at
from P import P

def is_blank(line):
  return not(line.strip())

WALL = "#"
EMPTY = "."
BOX = "O"
ROBOT = "@"

DIRECTIONS = {
  "<": P(-1,  0),
  ">": P( 1,  0),
  "^": P( 0, -1),
  "v": P( 0,  1)
}

class Warehouse(dict):
  def __init__(self, lines):
    for y, line in enumerate(lines):
      for x, char in enumerate(line.strip()):
        self[P(x, y)] = char
        if char == ROBOT:
          self.robot = P(x, y)
    self.size = P(x + 1, y + 1)

  def __str__(self):
    return "\n".join("".join(self[P(x, y)] for x in range(self.size.x)) for y in range(self.size.y))

  def move(self, direction, position = None):
    if position == None:
      position = self.robot

    nxt = position + direction
    if (obstacle := self[nxt]) == WALL:
      return False
    elif obstacle == ROBOT:
      raise ValueError
    elif obstacle == BOX:
      if not self.move(direction, nxt):
        return False

    # next position was (made) empty
    self[nxt] = self[position]
    self[position] = EMPTY
    if self[nxt] == ROBOT:
      self.robot = nxt
    return True

  def run(self, moves):
    for move in moves:
      self.move(DIRECTIONS[move])

  def coordinate_sum(self):
    return sum(p.x + 100 * p.y for p, tile in self.items() if tile == BOX)

def read_input():
  lines, moves = split_at(fileinput.input(), is_blank)
  warehouse = Warehouse(lines)
  moves = "".join(move.strip() for move in moves)
  return warehouse, moves
    
def main():
  warehouse, moves = read_input()

  # part 1
  warehouse.run(moves)
  print(warehouse.coordinate_sum())

if __name__ == "__main__":
  main()
