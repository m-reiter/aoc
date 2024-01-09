#!/usr/bin/python3

import fileinput

from attr import attrs, attrib
from termcolor import colored
from collections import deque

from P import P

FOREST = colored("#", "green")
PATH= "."

FANCY = { PATH: "O" }

NORTH = P(0, -1)
SOUTH = P(0, 1)
WEST = P(-1, 0)
EAST = P(1, 0)

SLOPES = {
  "^": NORTH,
  "v": SOUTH,
  "<": WEST,
  ">": EAST
}

@attrs
class Map:
  paths = attrib(factory = list)
  slopes = attrib(factory = dict)
  start = attrib(default = None)
  destination = attrib(default = None)
  size = attrib(default = None)
  longest_hike = attrib(default = None)

  def __getitem__(self, key):
    if key in self.slopes:
      return self.slopes[key]
    elif key in self.paths:
      return PATH
    else:
      return FOREST

  def __contains__(self, point):
    return point in list(self.slopes.keys()) + self.paths

  def __str__(self):
    return "\n".join(
      "".join(self[P(x, y)] for x in range(self.size.x))
      for y in range(self.size.y)
    )

  @classmethod
  def from_input(cls):
    paths = []
    slopes = {}

    for y, line in enumerate(fileinput.input()):
      for x, char in enumerate(line.strip()):
        if char == PATH:
          paths.append(P(x, y))
          if y == 0:
            start = P(x, y)
          else:
            destination = P(x, y)
        elif char in SLOPES:
          slopes[P(x, y)] = char

    return cls(paths, slopes, start, destination, P(x + 1, y + 1))

  def find_longest_hike(self):
    hikes = []
    strolls = deque([[ self.start ]])
    cache = {}
#    print(strolls)

    while strolls:
      stroll = strolls.popleft()
      current_position = stroll[-1]
      if current_position in cache and cache[current_position] > len(stroll):
        continue
      cache[current_position] = len(stroll)
      if current_position == self.destination:
        hikes.append(stroll)
        continue
      if current_position in self.paths:
        next_steps = [ p for p in current_position.get_neighbors(diagonals = False) if p in self and not p in stroll ]
      else:
        next_steps = [ current_position + SLOPES[self[current_position]] ]
        assert next_steps[0] in self
        if next_steps[0] in stroll:
          continue
      strolls.extend(stroll + [ step ] for step in next_steps)

    self.longest_hike = max(hikes, key = list.__len__)

  def print_hike(self):
    for y in range(self.size.y):
      for x in range(self.size.x):
        field = self[P(x, y)]
        print(colored(FANCY.get(field, field), "red") if P(x, y) in self.longest_hike else field, end = "")
      print()
    
def main():
  map = Map.from_input()
  print(map)
  print()

  # part 1
#  map.find_longest_hike()

#  map.print_hike()
#  print()
#  print(len(map.longest_hike) - 1)
#  print()

  # part 2
  map.paths.extend(map.slopes.keys())
  
  map.find_longest_hike()

  map.print_hike()
  print()
  print(len(map.longest_hike) - 1)

if __name__ == "__main__":
  main()
