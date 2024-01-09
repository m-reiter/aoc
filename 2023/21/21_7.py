#!/usr/bin/python3

import fileinput

from attr import attrs, attrib
from termcolor import colored
from collections import deque

from P import P

START = "S"
GARDEN = "."
ROCK = "#"
POSITION = "O"

FANCY = {
  START : colored(START, "yellow"),
  GARDEN : colored(GARDEN, "green"),
  ROCK : colored(ROCK, "white"),
  POSITION : colored(POSITION, "red"),
}

@attrs
class Farm:
  start = attrib(default = None)
  size = attrib(default = None)
  steps = attrib(default = 0)
  rocks = attrib(factory = list)
  distances = attrib(factory = dict)

  @classmethod
  def from_input(cls):
    farm = cls()

    for y, line in enumerate(fileinput.input()):
      for x, char in enumerate(line.strip()):
        if char == ROCK:
          farm.rocks.append(P(x, y))
        elif char == START:
          farm.start = P(x, y)

    farm.size = P(x, y)

    return farm

  def __str__(self):
  
    return "\n".join(
      "".join(FANCY[ROCK] if P(x, y) in self.rocks else
              FANCY[POSITION] if P(x, y) in self.positions else
              FANCY[START] if P(x, y) == self.start else
              FANCY[GARDEN]
              for x in range(self.size.x + 1)
             ) for y in range(self.size.y + 1))

  def calculate_distances(self):
    steps = 0
    positions = [ self.start ]

    while positions:
      for position in positions:
        self.distances[position] = steps
      neighbors = { n for x in positions for n in x.get_neighbors(diagonals = False, borders = self.size) }

      positions = [ position for position in neighbors
                    if not position in self.rocks
                    and not position in self.distances
                  ]

      steps += 1

  @property
  def positions(self):
    if not self.steps:
      return []
    return [ point for point, distance in self.distances.items() if distance % 2 == self.steps % 2 and distance <= self.steps ]

  def multiply(self, factor):
    new_rocks = []
    for i in range(factor + 1):
      for j in range(factor + 1):
        if i or j:
          for rock in self.rocks:
            new_rocks.append(P(rock.x + i * (self.size.x + 1), rock.y + j * (self.size.y + 1)))

    self.rocks.extend(new_rocks)

    self.start = P(self.start.x + (factor - 1) // 2 * (self.size.x + 1),
                   self.start.y + (factor - 1) // 2 * (self.size.y + 1))

    self.size = P((self.size.x + 1) * factor - 1, (self.size.y + 1) * factor - 1)

def main():
  farm = Farm.from_input()
#  print(farm)
#  print()

  farm.multiply(7)
  farm.calculate_distances()
  edge = min(v for k,v in farm.distances.items() if k.x in (0, farm.size.x) or k.y in (0, farm.size.y))
  for i in range(1,edge + 1,2):
    farm.steps = i
    print("{:4} {:6}".format(i, len(farm.positions)))
  return
  # part 1
  farm.calculate_distances()
  farm.steps = 64
  print(farm)
  print()
  print(len(farm.positions))

if __name__ == "__main__":
  main()
