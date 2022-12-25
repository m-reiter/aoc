#!/usr/bin/python3

import fileinput
from collections import defaultdict

from P import P

LEFT = "<"
RIGHT = ">"
UP= "^"
DOWN = "v"
EMPTY = "."
WALL = "#"
ELVES = "E"

DIRECTIONS = [LEFT,UP,DOWN,RIGHT]

OFFSETS = {
  LEFT: P(-1,0),
  RIGHT: P(1,0),
  UP: P(0,-1),
  DOWN: P(0,1)
}

class Flat:

  def __init__(self,lines):
    self.width = len(lines[0].strip()) - 2
    self.entrance = P(lines[0].index(EMPTY) - 1, -1)
    self.elves = self.entrance
    self.height = len(lines) - 2
    self.exit = P(lines[-1].index(EMPTY) - 1, self.height)
    self.data = defaultdict(list)
    self.positions = set()
    self.minutes = 0

    lines.pop(0)
    lines.pop(-1)
    for y,line in enumerate(lines):
      for x,tile in enumerate(line.strip(WALL+"\n")):
        if tile != EMPTY:
          self.data[P(x,y)].append(tile)

  def __getitem__(self,key):
    if key == self.elves:
      return ELVES
    if key in (self.entrance,self.exit):
      return EMPTY
    if key.x == -1 or key.x == self.width or key.y == -1 or key.y == self.height:
      return WALL
    if key in self.data:
      if len(self.data[key]) == 1:
        return self.data[key][0]
      if len(self.data[key]) > 9:
        return TOO_MANY
      return str(len(self.data[key]))
    if 0 <= key.x < self.width and 0 <= key.y < self.height:
      return EMPTY
    return None
  
  def __repr__(self):
    lines = []
    for y in range(-1,self.height + 1):
      lines.append("".join(self[P(x,y)] for x in range(-1,self.width + 1)))
    return "\n".join(lines)

  def move_blizzards(self):
    new_blizzards = defaultdict(list)
    for position,blizzards in self.data.items():
      for blizzard in blizzards:
        new_blizzards[position.get_neighbors(diagonals=False,borders=P(self.width,self.height),cyclic=True)[DIRECTIONS.index(blizzard)]].append(blizzard)
    self.data = new_blizzards
    #print(self)

  def move_elves(self,spawn=None):
    if spawn is None:
      spawn = self.entrance+OFFSETS[DOWN]
    new_positions = set()
    if self[spawn] == EMPTY:
      new_positions.add(spawn)
    for position in self.positions:
      if self[position] == EMPTY:
        new_positions.add(position)
      new_positions |= {neighbor for neighbor in position.get_neighbors(diagonals=False,borders=P(self.width,self.height)) if self[neighbor] == EMPTY}
    self.positions = new_positions
    self.minutes += 1
      
def part1(flat):
  while flat.exit+OFFSETS[UP] not in flat.positions:
    flat.move_blizzards()
    flat.move_elves()
  return flat.minutes+1

def part2(flat,offset):
  flat.positions = set()
  while flat.entrance+OFFSETS[DOWN] not in flat.positions:
    flat.move_blizzards()
    flat.move_elves(spawn=flat.exit+OFFSETS[UP])
  flat.positions = set()
  return part1(flat)

def main():
  flat = Flat(list(fileinput.input()))

  solution1 = part1(flat)
  print(solution1)

  print(part2(flat,solution1))

if __name__ == "__main__":
  main()
