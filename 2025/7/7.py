#!/usr/bin/python3

import fileinput
from itertools import pairwise
from functools import cache

EMPTY = "."
START = "S"
SPLITTER = "^"
BEAM = "|"

class Manifold():
  def __init__(self, lines):
    self._lines = list(lines)
    self.init()

  def init(self):
    self.lines = [ list(line.strip()) for line in self._lines ]
    self.start = self.lines[0].index(START)

  def __str__(self):
    return "\n".join("".join(line) for line in self.lines)

  def propagate_part1(self):
    verbose = len(self.lines) < 50
    if verbose:
      print(self)
      print()
    self.lines[1][self.start] = BEAM
    if verbose:
      print(self)
      print()
    splits = 0
    for current_line, next_line in pairwise(self.lines[1:]):
      for column, character in enumerate(current_line):
        if character == BEAM:
          if next_line[column] == SPLITTER:
            splits += 1
            next_line[column - 1] = BEAM
            next_line[column + 1] = BEAM
          else: # empty or beam from preceding splitter
            next_line[column] = BEAM
      if verbose:
        print(self)
        print()
    return splits

  @cache
  def count_timelines(self, start = None):
    if start is None:
      start = (1,self.start)
    line_no, column = start
    if line_no == len(self.lines) - 1:
      return 1
    elif self.lines[line_no + 1][column] == EMPTY:
      return self.count_timelines((line_no + 1, column))
    else: # we must have hit a splitter
      return self.count_timelines((line_no + 1, column - 1)) + self.count_timelines((line_no + 1, column + 1))

def main():
  manifold = Manifold(fileinput.input())

  # part 1
  print(manifold.propagate_part1())

  # part 2
  manifold.init()
  print(manifold.count_timelines())

if __name__ == "__main__":
  main()
