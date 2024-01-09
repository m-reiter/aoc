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
    scan, *checksums = line.strip().split()
    self._scan = scan
    if checksums:
      self.checksums = tuple(map(int, checksums[0].split(",")))
    else:
      self.checksums = tuple()
    self.unknown = scan.count(UNKNOWN)
    self.missing = sum(self.checksums) - scan.count(DAMAGED)
    # consecutive blocks of unknowns, separated only by damaged springs
    self.blocks = self.get_blocks(scan)
    # replace all unknowns with their index for replacing
    positions = deque(range(len(scan)))
    self.scan = [ positions.popleft() if char == UNKNOWN else char for char in scan ]
    self._line = line.strip()

  def __repr__(self):
    return 'Row("{}")'.format(self._line)

  def get_blocks(self, scan):
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
    states = [ self ]

    possibilities = 0
    while states:
      next_states = []
      for state in states:
        next_states.extend(state.place_group())

      possibilities += sum(state.is_solution() for state in next_states)
      states = [ state for state in next_states if not state.is_solution() ]

    return possibilities

  def unfold(self):
    scan, checksums = self._line.split()
    scan = UNKNOWN.join([ scan ] * 5)
    checksums = ",".join([ checksums ] * 5)
    return Row("{} {}".format(scan, checksums))

  def place_group(self, found = 0):
    # find all ways to match the first group
    try:
      group, *to_match = self.checksums
    except ValueError:
      return []
    to_match = ",".join(map(str, to_match))
    results = []
    replacements = []
    max_to_check = self.unknown
    if self.matches(self.scan, single = True):
      left, _, right = self._scan.partition(DAMAGED)
      blocks = self.get_blocks(left[:-1])
      remainder = right[group:] or OPERATIONAL
      results.append(Row("{} {}".format(remainder, to_match)))
    else: blocks = self.blocks
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
            remainder = remainder[1:] or OPERATIONAL
            results.append(Row("{} {}".format(remainder, to_match)))
      current += block

    return results

def main():
  conditions = [ Row(line) for line in fileinput.input() ]

  # part 1
  print(sum(map(Row.count_possibilities, conditions)))

  # part 2
  conditions = list(map(Row.unfold, conditions))
  total = 0
  for i, condition in enumerate(conditions):
    possibilities = condition.count_possibilities()
    print(i,condition,possibilities)
    total += possibilities
  print(total)

if __name__ == "__main__":
  main()
