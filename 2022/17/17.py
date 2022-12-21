#!/usr/bin/python3

import fileinput
from more_itertools import pairwise
from collections import UserDict

from P import P

DEBUG = 0

ROCKS = """####

.#.
###
.#.

..#
..#
###

#
#
#
#

##
##"""

ROCK = "#"
FALLING = "@"
EMPTY = "."
WALL = "|"
FLOOR = "-"
CORNER = "+"

class Cycle:
  def __init__(self,data):
    self.position = -1
    self.data = data

  def __iter__(self):
    return self

  def __next__(self):
    self.position = (self.position + 1) % len(self)
    return self.data[self.position]

  def __len__(self):
    return len(self.data)

class Rock(UserDict):
  
  def __init__(self,pattern):
    super().__init__()
    for y,line in enumerate(reversed(pattern.split("\n"))):
      for x,char in enumerate(line):
        self[P(x,y)] = char == ROCK
    self.width = max(key.x for key in self.keys())+1
    self.height = max(key.y for key in self.keys())+1

  def bottom(self,x):
    return min(key.y for key in self.keys() if self[key] and key.x == x)

  def top(self,x):
    return max(key.y for key in self.keys() if self[key] and key.x == x)

  def left(self,y):
    return min(key.x for key in self.keys() if self[key] and key.y == y)

  def right(self,y):
    return max(key.x for key in self.keys() if self[key] and key.y == y)

  def __repr__(self):
    lines = []
    for y in range(self.height):
      lines.append("".join("#" if self[P(x,y)] else "." for x in range(self.width)))
    return "\n".join(reversed(lines))

class Cave(UserDict):

  def __init__(self,width=7):
    super().__init__()
    self.width = width
    self.height = 0
    self.falling_rock = None
    self.position = None

  def __getitem__(self,key):
    try:
      if self.falling_rock is not None and self.falling_rock[key-self.position]:
        return FALLING
    except KeyError:
      pass
    try:
      return self.data[key]
    except KeyError:
      if key.x == -1 or key.x == self.width:
        return CORNER if key.y == -1 else WALL
      elif key.y == -1:
        return FLOOR
      else:
        return EMPTY

  def top_shape(self):
    tops = [max((key.y for key in self.keys() if key.x == x),default=0) for x in range(self.width)]
    start = min(tops)
    top_shape = set(key-P(0,start) for key in self.keys() if key.y >= start)
    return top_shape

  def add_rock(self,rocks,jets):
    if DEBUG: print("adding rock")
    self.falling_rock = rock = next(rocks)
    self.position = position = P(2,self.height+3)
    if DEBUG: print(self)
    while True:
      jet = next(jets)
      # move sidewards
      if DEBUG >= 2: print("pushing","left" if jet == "<" else "right")
      direction = -1 if jet == "<" else 1
      edge = rock.left if jet == "<" else rock.right
      if not any(self[P(position.x+edge(y)+direction,position.y+y)] != EMPTY for y in range(rock.height)):
        self.position = position = P(position.x+direction,position.y)
      if DEBUG >= 2: print(self)
      # try to fall down
      if not any(self[P(position.x+x,position.y+rock.bottom(x)-1)] != EMPTY for x in range(rock.width)):
        if DEBUG >= 2: print("falling")
        self.position = position = P(position.x,position.y-1)
        if DEBUG >= 2: print(self)
      else:
        if DEBUG >= 2: print("landed")
        for x in range(rock.width):
          for y in range(rock.height):
            if rock[P(x,y)]:
              self[P(position.x+x,position.y+y)] = ROCK
        self.height = max(self.height,position.y+rock.height)
        self.falling_rock = None
        if DEBUG >= 2: print(self)
        break

  def __repr__(self):
    lines = []
    maxy = self.height+3
    if self.falling_rock is not None:
      maxy += self.falling_rock.height
    for y in range(-1,maxy):
      lines.append("".join(self[P(x,y)] for x in range(-1,self.width+1)))
    return "\n".join(reversed(lines))

def parse_rocks():
  rocks = []
  for pattern in ROCKS.split("\n\n"):
    rocks.append(Rock(pattern))
  return rocks

def part1(rocks,jets):
  cave = Cave()
  rocks = Cycle(rocks)
  jets = Cycle(jets)
  for _ in range(2022):
    cave.add_rock(rocks,jets)
  print(cave)
  return cave.height

def part2(rocks,jets):
  cave = Cave()
  rocks = Cycle(rocks)
  jets = Cycle(jets)
  top_shapes = {}
  fallen = 0
  while True:
    cave.add_rock(rocks,jets)
    fallen += 1
    top_shape = cave.top_shape()
    top_shape.add((rocks.position,jets.position))
    top_shape = tuple(top_shape)
    if top_shape in top_shapes.keys():
      height_before,fallen_before = top_shapes[top_shape]
      height_gain = cave.height - height_before
      period = fallen - fallen_before
      moves_left = 1000000000000 - fallen
      periods = moves_left // period
      for _ in range(moves_left % period):
        cave.add_rock(rocks,jets)
      print(cave)
      return cave.height + periods * height_gain
    else:
      top_shapes[top_shape] = (cave.height,fallen)
  return cave.height

def main():
  rocks = parse_rocks()
  jets = fileinput.FileInput().readline().strip()

  print(part1(rocks,jets))
  print(part2(rocks,jets))

if __name__ == "__main__":
  main()
