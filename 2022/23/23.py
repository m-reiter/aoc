#!/usr/bin/python3

import fileinput
from collections import UserDict
from itertools import cycle

from P import P

ELF = "#"
EMPTY = "."
PROPOSING = "*"

NORTH = P(0,-1)
SOUTH = P(0,1)
WEST = P(-1,0)
EAST = P(1,0)

DIRECTIONS = [NORTH, SOUTH, WEST, EAST]
class Grove(UserDict):
  
  def __init__(self,area_map):
    super().__init__()
    for y,line in enumerate(area_map):
      for x,plot in enumerate(line):
        if plot == ELF:
          self[P(x,y)] = ELF
    self.proposing = {}
    self.starting_directions = cycle(range(len(DIRECTIONS)))

  def __getitem__(self,key):
    if key in self.proposing:
      return PROPOSING
    try:
      return self.data[key]
    except KeyError:
      return EMPTY

  def dimensions(self):
    xmin = min(key.x for key in self)-bool(self.proposing)
    xmax = max(key.x for key in self)+bool(self.proposing)
    ymin = min(key.y for key in self)-bool(self.proposing)
    ymax = max(key.y for key in self)+bool(self.proposing)
    return xmin,xmax,ymin,ymax

  def __repr__(self):
    xmin,xmax,ymin,ymax = self.dimensions()
    lines = ["".join(self[P(x,y)] for x in range(xmin,xmax+1)) for y in range(ymin,ymax+1)]
    return "\n".join(lines)

  def move(self):
    starting_direction = next(self.starting_directions)
    for elf in self:
      neighbors = elf.get_neighbors()
      if any(key in self for key in neighbors):
        for i in range(len(DIRECTIONS)):
          direction = DIRECTIONS[(starting_direction + i) % len(DIRECTIONS)]
          candidates = [elf+offset for offset in P.offsets() if offset.x*direction.x == abs(direction.x) and offset.y*direction.y == abs(direction.y)]
          if not any(candidate in self for candidate in candidates):
            destination = elf+direction
            if destination in self.proposing:
              self.proposing[destination] = None
            else:
              self.proposing[destination] = elf
            break
    #print()
    #print(self)
    moves = [(elf,destination) for destination,elf in self.proposing.items() if elf is not None]
    self.proposing = {}
    if not moves:
      return False
    for elf,destination in moves:
      self.pop(elf)
      self[destination] = ELF
    return True
    #print()
    #print(self)

def part1(grove):
  for _ in range(10):
    grove.move()
  print(grove)
  xmin,xmax,ymin,ymax = grove.dimensions()
  return (xmax-xmin+1) * (ymax-ymin+1) - len(grove)

def part2(grove,moves=11):
  while grove.move():
    if moves % 10 == 0:
      print(grove)
      print(moves)
    moves += 1
  print(grove)
  return moves

def main():
  grove = Grove(fileinput.input())

  #print(part1(grove))
  print(part2(grove,1))

if __name__ == "__main__":
  main()
