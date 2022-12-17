#!/usr/bin/python3

import fileinput
from collections import defaultdict
from more_itertools import pairwise
from numpy import sign

from P import P

START = P(500,0)
SOURCE = '+'
EMPTY = '.'
ROCK = '#'
SAND = 'o'

class Cave:

  def __init__(self,paths):
    self.cave = defaultdict(lambda: EMPTY)
    self.cave[START] = SOURCE
    self.minx = self.maxx = START.x
    self.miny = self.maxy = START.y
    self.sand = 0
    self.floor = False

    for path in paths:
      nodes = [P(*(int(coord) for coord in node.split(","))) for node in path.strip().split(" -> ")]
      self.minx = min(self.minx,min(node.x for node in nodes))
      self.maxx = max(self.maxx,max(node.x for node in nodes))
      self.miny = min(self.miny,min(node.y for node in nodes))
      self.maxy = max(self.maxy,max(node.y for node in nodes))
      for start,end in pairwise(nodes):
        vector = P(*(sign(coord) for coord in end+ -1*start))
        self.cave[start] = ROCK
        while start != end:
          start += vector
          self.cave[start] = ROCK
    
    print(self)    

  def add_floor(self):
    self. maxy += 2
    for x in range(self.minx,self.maxx+1):
      self.cave[P(x,self.maxy)] = ROCK
    self.floor = True

  def trickle(self):
    sand = START
    while True:
      if self.floor and sand.y == self.maxy-1:
        for x in range(sand.x-1,sand.x+2):
          self.cave[P(x,self.maxy)] = ROCK
      for vector in [P(0,1),P(-1,1),P(1,1)]:
        if self.cave[sand+vector] == EMPTY:
          sand += vector
          if sand.y > self.maxy or not (self.minx <= sand.x <= self.maxx or self.floor):
            return False
          break
      else:
        self.cave[sand] = SAND
        self.sand += 1
        self.minx = min(self.minx,sand.x)
        self.maxx = max(self.maxx,sand.x)
        return sand != START
        
  def __repr__(self):
    repr = []
    for y in range(min(0,self.miny),self.maxy+1):
      repr.append("".join(self.cave[P(x,y)] for x in range(self.minx,self.maxx+1)))
    return "\n".join(repr)

def main():
  paths = list(fileinput.input())

  # part 1
  cave = Cave(paths)
  while(cave.trickle()):
    pass
  print()
  print(cave)
  print(cave.sand)
  
  # part 2
  print()
  cave = Cave(paths)
  cave.add_floor()
  while(cave.trickle()):
    pass
  print()
  print(cave)
  print(cave.sand)
  

if __name__ == "__main__":
  main()
