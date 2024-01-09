#!/usr/bin/python3

import fileinput

from more_itertools import run_length
from collections import deque
from itertools import combinations

OPERATIONAL = "."
DAMAGED = "#"
UNKNOWN = "?"

SAMPLE_LINE = "???.### 1,1,3"

class Translation(set):
  def __getitem__(self, key):
    return DAMAGED if key in self else key

  def translate(self, scan):
    return [ self[char] for char in scan ]

class Row:
  def __init__(self, line):
    scan, checksums = line.strip().split()
    self.checksums = tuple(map(int, checksums.split(",")))
    self.unknown = scan.count(UNKNOWN)
    self.missing = sum(self.checksums) - scan.count(DAMAGED)
    positions = deque(range(len(scan)))
    self.scan = [ positions.popleft() if char == UNKNOWN else char for char in scan ]
    self._line = line.strip()

  def __repr__(self):
    return 'Row("{}")'.format(self._line)

  def matches(self, scan):
    return self.checksums == tuple(length for value, length in run_length.encode(scan) if value == DAMAGED)

  def count_possibilities(self):
    return sum(self.matches(Translation(replacements).translate(self.scan))
               for replacements in combinations(range(self.unknown), self.missing))

  def unfold(self):
    scan, checksums = self._line.split()
    scan = UNKNOWN.join([ scan ] * 5)
    checksums = ",".join([ checksums ] * 5)
    return Row("{} {}".format(scan, checksums))

def main():
  conditions = [ Row(line) for line in fileinput.input() ]

  # part 1
  print(sum(map(Row.count_possibilities, conditions)))

if __name__ == "__main__":
  main()
