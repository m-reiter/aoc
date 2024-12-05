#!/usr/bin/python3

import fileinput
from collections import defaultdict

from P import P

EMPTY = "."

class Grid:
  def __init__(self, lines):
    self._lines = [line.strip() for line in lines]
    if len(set(map(len, self._lines))) != 1:
      raise(ValueError, "Not a rectangular grid")
    self.width = len(self._lines[0])
    self.height = len(self._lines)

  def __str__(self):
    return "\n".join(self._lines)

  def __repr__(self):
    return f"<word search grid (size {self.width}x{self.height}>"

  def __getitem__(self, pos):
    if (0 <= pos.x < self.width) and (0 <= pos.y < self.height):
      return self._lines[pos.y][pos.x]
    return EMPTY

  def find_word(self, word, offsets):
    directions = [[offset * i for i in range(1, len(word))] for offset in offsets]

    found = defaultdict(int)
    
    for x in range(self.width):
      for y in range(self.height):
        if self[P(x,y)] == word[0]:
          for direction in directions:
            if "".join(self[P(x,y) + offset] for offset in direction) == word[1:]:
              found[P(x,y) + direction[0]] += 1

    return found

def main():
  grid = Grid(fileinput.input())

  # part 1
  print(sum(grid.find_word("XMAS", P.offsets()).values()))

  # part 2
  # diagonal directions only for X-MASes
  offsets = [P(x,y) for x in (-1,1) for y in (-1,1)]
  #print(grid.find_word("MAS", offsets))
  print(len([x for x in grid.find_word("MAS", offsets).values() if x == 2]))

if __name__ == "__main__":
  main()
