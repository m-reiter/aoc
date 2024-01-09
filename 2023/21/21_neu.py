#!/usr/bin/python3

# (steps + 1)**2-(steps//unit-1)**2*Gerade-(steps//unit)**2*Ungerade-(2*Gerade+2*Gerade_Mitte)-(steps//unit-1)*(4*Gerade-1*Gerade_Ecken)-(steps//unit)*Ungerade_Ecken

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
  GARDEN : (colored(GARDEN, "green"), colored(GARDEN, "white")),
  ROCK : colored(ROCK, "white"),
  POSITION : colored(POSITION, "red"),
}

EVEN = 0
ODD = 1

@attrs
class Farm:
  start = attrib(default = None)
  size = attrib(default = None)
  steps = attrib(default = 0)
  rocks = attrib(factory = list)
  even_rocks = attrib(default = None)
  odd_rocks = attrib(default = None)
  distances = attrib(factory = dict)
  positions = attrib(default = None)
  unit = attrib(default = 1)

  @classmethod
  def from_input(cls):
    farm = cls()

    for y, line in enumerate(fileinput.input()):
      for x, char in enumerate(line.strip()):
        if char == ROCK:
          farm.rocks.append(P(x, y))
        elif char == START:
          start = P(x, y)

    farm.size = P(x, y)

    farm.set_start(start)
    farm.calculate_positions()

    assert x == y
    farm.unit = x + 1

    return farm

  def __str__(self):
  
    return "\n".join(
      "".join(FANCY[ROCK] if P(x, y) in self.rocks else
              FANCY[POSITION] if P(x, y) in self.positions else
              FANCY[START] if P(x, y) == self.start else
              FANCY[GARDEN][(x // self.unit + y // self.unit) % 2]
              for x in range(self.size.x + 1)
             ) for y in range(self.size.y + 1))

  def analyse(self, steps = 26501365):
    # find unaccessible spaces
    self.set_steps(2 * self.unit)
    unaccessible = [ P(x,y) for x in range(self.unit) for y in range(self.unit) if (x + y) % 2 == EVEN and P(x,y) not in self.rocks and P(x,y) not in self.positions ]
    self.set_steps(2 * self.unit + 1)
    unaccessible.extend([ P(x,y) for x in range(self.unit) for y in range(self.unit) if (x + y) % 2 == ODD and P(x,y) not in self.rocks and P(x,y) not in self.positions ])
    self.rocks.extend(unaccessible)

    self.even_rocks = { rock for rock in self.rocks if (rock.x + rock.y) % 2 == EVEN }
    self.odd_rocks = { rock for rock in self.rocks if (rock.x + rock.y) % 2 == ODD }

    self.center_rocks = { rock for rock in self.rocks
                          if self.size.y // 2 - rock.x < rock.y < self.size.y // 2 + rock.x
                          and -self.size.x // 2 + rock.x < rock.y < self.size.y + self.size.x // 2 - rock.x }

    assert steps % self.unit == self.size.x / 2
    assert (steps // self.unit) % 2 == EVEN

    # (steps + 1)**2-(steps//unit-1)**2*Gerade-(steps//unit)**2*Ungerade-(2*Gerade+2*Gerade_Mitte)-(steps//unit-1)*(4*Gerade-1*Gerade_Ecken)-(steps//unit)*Ungerade_Ecken
    # *EDIT*: Beim Abzaehlen Gerade und Ungerade vertauscht...
    area = (steps + 1)**2
    area -= (steps // self.unit - 1)**2 * len(self.odd_rocks)
    area -= (steps // self.unit)**2 * len(self.even_rocks)
    area -= 2 * (len(self.odd_rocks) + len(self.odd_rocks & self.center_rocks))
    area -= (steps // self.unit - 1) * (4 * len(self.odd_rocks) - len(self.odd_rocks - self.center_rocks))
    area -= (steps // self.unit) * len(self.even_rocks - self.center_rocks)

    return area
    
  def calculate_distances(self):
    steps = 0
    positions = [ self.start ]
    self.distances = dict()

    while positions:
      for position in positions:
        self.distances[position] = steps
      neighbors = { n for x in positions for n in x.get_neighbors(diagonals = False, borders = self.size) }

      positions = [ position for position in neighbors
                    if not position in self.rocks
                    and not position in self.distances
                  ]

      steps += 1

  def calculate_positions(self):
    if not self.steps:
      self.positions = []
    else:
      self.positions = [ point for point, distance in self.distances.items() if distance % 2 == self.steps % 2 and distance <= self.steps ]

  def set_steps(self, steps):
    self.steps = steps
    self.calculate_positions()

  def set_start(self, start):
    self.start = P(*start)
    self.calculate_distances()

  def multiply(self, factor):
    new_rocks = []
    for i in range(factor + 1):
      for j in range(factor + 1):
        if i or j:
          for rock in self.rocks:
            new_rocks.append(P(rock.x + i * (self.size.x + 1), rock.y + j * (self.size.y + 1)))

    self.rocks.extend(new_rocks)

    self.set_start(P(self.start.x + (factor - 1) // 2 * (self.size.x + 1),
                     self.start.y + (factor - 1) // 2 * (self.size.y + 1)))

    self.size = P((self.size.x + 1) * factor - 1, (self.size.y + 1) * factor - 1)

def main():
  farm = Farm.from_input()
  print(farm)
  print()

  # part 1
  farm.calculate_distances()
  farm.set_steps(64)
  print(farm)
  print()
  print(len(farm.positions))

  # part 2
  print()
  print(farm.analyse())

if __name__ == "__main__":
  main()
