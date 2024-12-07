#!/usr/bin/python3

import fileinput
from collections import defaultdict
from itertools import cycle

from P import P

EMPTY = "."
OBSTRUCTION = "#"
GUARD = "^"
OUTSIDE = " "

DIRECTIONS = {
  P( 0,-1): "^",
  P( 1, 0): ">",
  P( 0, 1): "v",
  P(-1, 0): "<"
}

class Map:
  def __init__(self, lines):
    self._map = defaultdict(lambda: OUTSIDE)
    for y, line in enumerate(lines):
      for x, symbol in enumerate(line.strip()):
        if symbol == GUARD:
          symbol = EMPTY
          self.start = P(x,y)
        self._map[P(x,y)] = symbol

    self.width = x + 1
    self.height = y + 1
    self.reset()

  def reset(self):
    self.guard = self.start
    self.turns = cycle(DIRECTIONS)
    self.direction = next(self.turns)
    self.visited = defaultdict(set)

  def __repr__(self):
    return f"<Map ({self.width}x{self.height}), guard ({DIRECTIONS[self.direction]}) at {self.guard}>"

  def step(self):
    if (ahead := self._map[self.guard + self.direction]) == OBSTRUCTION:
      self.direction = next(self.turns)
    else:
      self.guard = self.guard + self.direction

  def run(self):
    while True:
      self.visited[self.guard].add(self.direction)
      self.step()
      if self._map[self.guard] == OUTSIDE:
        return False
      if self.direction in self.visited[self.guard]:
        # loop detected
        return True

  def find_loops(self, previous_path):
    loops = 0

    for i,point in enumerate(previous_path):
      if point == self.start:
        continue
      self.reset()
      self._map[point] = OBSTRUCTION
      if self.run():
        loops += 1
      self._map[point] = EMPTY

    return loops


def main():
  lab = Map(fileinput.input())

  # part 1
  lab.run()
  print(len(lab.visited))

  # part 2
  print(lab.find_loops(lab.visited))

if __name__ == "__main__":
  main()
