#!/usr/bin/python3

import fileinput
import attr

@attr.s
class Position:
  x = attr.ib()
  y = attr.ib()
  aim = attr.ib(default=0)

  def __add__(self, other):
    return Position(self.x+other.x, self.y+other.y, self.aim+other.aim)

  def __mul__(self, other):
    return Position(self.x*other, self.y*other, self.aim*other)

  def __rmul__(self, other):
    return self.__mul__(other)

DIRECTIONS = {
  'forward': Position(1,0),
  'up': Position(0,-1),
  'down': Position(0,1)
}

def main():
  data = list(fileinput.input())

  position = Position(0,0)

  for line in data:
    direction, steps = line.split()
    position += DIRECTIONS[direction]*int(steps)

  print(position)
  print(position.x*position.y)

  position = Position(0,0)

  DIRECTIONS['up'] = Position(0,0,-1)
  DIRECTIONS['down'] = Position(0,0,1)
  
  for line in data:
    DIRECTIONS['forward'] = Position(1,position.aim)
    direction, steps = line.split()
    position += DIRECTIONS[direction]*int(steps)

  print(position)
  print(position.x*position.y)

if __name__ == "__main__":
  main()
