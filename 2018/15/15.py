#!/usr/bin/python3

import fileinput
from collections import UserDict

from P import P

ELF = 0
GOBLIN = 1

UNITS = {
  "E": ELF,
  "G": GOBLIN
}

WALL = "#"
OPEN = "."

class Unit:
  def __init__(self,kind):
    self.kind = kind
    self.attack = 3
    self.hp = 200

class Cave(UserDict):
  def __init__(self):
    super().__init__()
    self.units = [{}, {}]
    for y,line in enumerate(fileinput.input()):
      for x,char in enumerate(line.strip()):
        if char in UNITS:
          self.units[UNITS[char]][P(y,x)] = Unit(UNITS[char])
        elif char == WALL:
          self[P(y,x)] = WALL

  def __getitem__(self,key):
    for kind in self.units:
      if key in kind:
        return kind[key].kind
    if key in self:
      return WALL
    return OPEN

def main():
  pass

if __name__ == "__main__":
  main()
