#!/usr/bin/python3

import fileinput

from more_itertools import split_at
from collections import defaultdict

ASH = "."
ROCK = "#"
SWAP = {
  ASH:  ROCK,
  ROCK: ASH
}

def is_blank(line):
  return not line.strip()

class Pattern:
  def __init__(self):
    self._pattern = defaultdict(dict)
    self.dimx = None
    self.dimy = None

  @classmethod
  def from_lines(cls, lines):
    pattern = cls()

    for y, line in enumerate(lines):
      for x, char in enumerate(line.strip()):
        pattern[(x, y)] = char

    pattern.dimx = x + 1
    pattern.dimy = y + 1

    return pattern

  def __getitem__(self, key):
    x, y = key

    return self._pattern[x][y]

  def __setitem__(self, key, value):
    x, y = key

    self._pattern[x][y] = value

  def swap(self, x, y):
    self[(x,y)] = SWAP[self[(x,y)]]

  def row(self, index):
    return "".join(self[(x, index)] for x in range(self.dimx))
    
  def column(self, index):
    return "".join(self[(index, y)] for y in range(self.dimy))

  def is_symmetric(self, function, index, size):
    assert 1 <= index < size
    return all(function(index - 1 - i) == function(index + i) for i in range(min(index, size - index)))

  def get_symmetry_lines(self):
    lines = [
      set(
        weight * index * self.is_symmetric(function, index, size) for index in range(1, size)
      ) for weight, function, size in (
        (1, self.column, self.dimx),
        (100, self.row, self.dimy)
      )
    ]
    
    return set.union(*lines)
    
  def summarize(self):
    return sum(self.get_symmetry_lines())

  def fix_smudge(self):
    reference = self.get_symmetry_lines()

    for x in range(self.dimx):
      for y in range(self.dimy):
        self.swap(x, y)
        
        new_lines = self.get_symmetry_lines() - reference

        if new_lines:
          return new_lines.pop()

        self.swap(x, y)

def read_input():
  return [ Pattern.from_lines(lines) for lines in split_at(fileinput.input(), is_blank) ]

def main():
  patterns = read_input()

  # part 1
  print(sum(map(Pattern.summarize, patterns)))

  # part 1
  print(sum(map(Pattern.fix_smudge, patterns)))

if __name__ == "__main__":
  main()
