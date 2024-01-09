#!/usr/bin/python3

import fileinput

from more_itertools import run_length
from collections import deque, Counter
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
  def __init__(self, scan, checksums):
    self._scan = scan
    self.checksums = checksums
    self.unknown = scan.count(UNKNOWN)
    # consecutive blocks of unknowns, separated only by damaged springs
    self.blocks = Row.get_blocks(scan)
    # replace all unknowns with their index for replacing
    positions = deque(range(len(scan)))
    self.scan = [ positions.popleft() if char == UNKNOWN else char for char in scan ]

  @classmethod
  def from_line(cls, line):
    scan, *checksums = line.strip().split()
    if checksums:
      checksums = tuple(map(int, checksums[0].split(",")))
    else:
      checksums = tuple()
    return cls(scan, checksums)

  def __repr__(self):
    return 'Row("{}", {})'.format(self._scan, self.checksums)

  @staticmethod
  def get_blocks(scan):
    return tuple(length for value, length in run_length.encode(scan.replace(DAMAGED, "")) if value == UNKNOWN)

  def matches(self, scan, single = False):
    checksums = tuple(length for value, length in run_length.encode(scan) if value == DAMAGED)
    if single:
      try:
        return self.checksums[0] == checksums[0]
      except IndexError:
        return not self.checksums and not checksums
    else:
      return self.checksums == checksums

  def is_solution(self):
    return self.matches(self.scan)

  def count_possibilities(self):
    # state and number of ways to reach it
    states = [ (self, 1) ]
    to_match = self.checksums

    while to_match:
      next_states = Counter()
      for state, ways in states:
        next_states += state.place_group(ways)

      to_match = to_match[1:]

      states = [ (Row(state, to_match), count) for state, count in next_states.items() ]

    return sum(value for state, value in states if state.is_solution())

  def unfold(self):
    scan = UNKNOWN.join([ self._scan ] * 5)
    checksums = self.checksums * 5
    return Row(scan, checksums)

  def place_group(self, ways):
    """
    return a Counter object of all remaining strings and the number of ways to reach them
    """
    group = self.checksums[0]

    results = []
    replacements = []

    if self.matches(self.scan, single = True):
      left, _, right = self._scan.partition(DAMAGED)
      blocks = Row.get_blocks(left[:-1])
      remainder = right[group:]
      results.append(remainder)
    else:
      blocks = self.blocks

    current = 0
    for block in blocks:
      max_length = min((block, group))
      for l in range(1, max_length + 1):
        for start in range(current, current + block + 1 - l):
          replacement = range(start, start + l)
          if self.matches(Translation(replacement).translate(self.scan), single = True):
            remainder = self._scan[self.scan.index(max(replacement)) + 1:]
            while remainder.startswith(DAMAGED):
              remainder = remainder[1:]
            remainder = remainder[1:]
            results.append(remainder)
      current += block

    outcomes = Counter(result.lstrip(OPERATIONAL) for result in results)
    multiplied = Counter({ key: value * ways for key, value in outcomes.items() })

    return multiplied

def main():
  conditions = [ Row.from_line(line) for line in fileinput.input() ]

  # part 1
  print(sum(map(Row.count_possibilities, conditions)))

  # part 2
  conditions = list(map(Row.unfold, conditions))

  print(sum(map(Row.count_possibilities, conditions)))

if __name__ == "__main__":
  main()
