#!/usr/bin/python3

import fileinput
import re

from collections import defaultdict
from more_itertools import pairwise

from P import P

PLAN = re.compile("([UDLR]) (\d+) \(#(\w{5})(\w)\)")

DIRECTIONS = {
  "U": P(0, -1),
  "D": P(0, 1),
  "L": P(-1, 0),
  "R": P(1, 0)
}
INT_TO_DIRECTION = "RDLU"

class Horizontal:
  def __init__(self, start, end):
    self.start = start
    self.end = end
    self.crossing = None

  def __repr__(self):
    return "<{}Horizontal ({},{})>".format("Crossing " if self.crossing else "", self.start, self.end)

  def __len__(self):
    return self.end - self.start + 1

class Vertical:
  def __init__(self, direction, position, start, end):
    self.direction = direction
    self.position = position
    self.start = start
    self.end = end

  def __repr__(self):
    return "<Vertical at column {} ({},{})>".format(self.position, self.start, self.end)

class Dig():
  def __init__(self):
    self.changes = { 0 }
    self.horizontals = defaultdict(list)
    self.verticals = []

  @classmethod
  def from_input(cls, corrected = False):
    dig = cls()

    position = P(0, 0)
    horizontals = []
    previous_vertical = None

    for line in fileinput.input():
      direction, length, hexlength, hexdirection = PLAN.match(line).groups()

      if corrected:
        direction = INT_TO_DIRECTION[int(hexdirection)]
        length = int(hexlength, 16)
      else:
        length = int(length)

      new_position = position + DIRECTIONS[direction] * length
      
      if direction in "UD": # vertical
        start, end = sorted(p.y for p in (position, new_position))

        dig.verticals.append(Vertical(direction, position.x, start, end))
        dig.changes.add(new_position.y)

        if previous_vertical:
          horizontals[-1][1].crossing = direction == previous_vertical

        previous_vertical = direction

      else: # horizontal
        start, end = sorted(p.x for p in (position, new_position))

        horizontals.append((position.y, Horizontal(start, end)))

      position = new_position
    
    if horizontals[0][1].crossing is None: # first line was horizontal
      missing = horizontals[0][1]
    else:
      missing = horizontals[-1][1]

    missing.crossing = dig.verticals[0].direction == dig.verticals[-1].direction

    for y, horizontal in horizontals:
      dig.horizontals[y].append(horizontal)

    return dig

  def line_volume(self, y):
    sections = { (v.position, v.position, True) for v in self.verticals if v.start < y < v.end }

    sections = sorted(sections.union((h.start, h.end, h.crossing) for h in self.horizontals[y]))

    start, end, in_dig = sections[0]

    volume = end - start + 1

    for first, second in pairwise(sections):
      volume += in_dig * (second[0] - first[1] - 1)
      volume += second[1] - second[0] + 1
      if second[2]:
        in_dig = not in_dig

    return volume

  def total_volume(self):
    volume = self.line_volume(min(self.changes))

    for start, end in pairwise(sorted(self.changes)):
      volume += self.line_volume(start + 1) * (end - start - 1)
      volume += self.line_volume(end)

    return volume

def main():

  # part 1
  dig = Dig.from_input()
  print(dig.total_volume())

  # part 2
  dig = Dig.from_input(corrected = True)
  print(dig.total_volume())

if __name__ == "__main__":
  main()
