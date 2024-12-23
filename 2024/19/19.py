#!/usr/bin/python3

import fileinput
from more_itertools import split_at
from functools import cache

def is_blank(line):
  return not(line.strip())

class Towels:
  def __init__(self, patterns):
    self.patterns = patterns

  @cache
  def count_possibilities(self, design):
    if len(design) == 0:
      return 1
    candidates = [ p for p in self.patterns if design.startswith(p) ]
    return sum(self.count_possibilities(design[len(c):]) for c in candidates)

def get_input():
  patterns, designs = split_at(fileinput.input(), is_blank)
  towels = Towels([ p.strip() for p in patterns[0].split(", ") ])
  designs = [ design.strip() for design in designs ]
  return towels, designs

def main():
  towels, designs = get_input()

  possibilities = [ towels.count_possibilities(design) for design in designs ]

  # part 1
  print(sum([ p > 0 for p in possibilities ]))

  # part 2
  print(sum(possibilities))

if __name__ == "__main__":
  main()
