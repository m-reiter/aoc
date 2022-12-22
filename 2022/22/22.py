#!/usr/bin/python3

import fileinput
from itertools import groupby
from more_itertools import split_at
from collections import UserDict

from P import P

DIRECTIONS = [P(1,0),P(0,1),P(-1,0),P(0,-1)]
TRACES = [">","v","<","^"]
WALL = "#"
POSITION = "@"

def is_blank(line):
  return line.strip() == ""

class Board(UserDict):
  def __init__(self,lines):
    super().__init__()
    self.width = {}
    self.height = {}
    self.facing = 0
    for y,line in enumerate(lines,1):
      tiles = [(x,kind) for x,kind in enumerate(line.rstrip(),1) if kind.strip()]
      for x,kind in tiles:
        self[P(x,y)] = kind
      self.width[y] = (min(_[0] for _ in tiles),max(_[0] for _ in tiles))
    for x in range(1,max(w[1] for w in self.width.values())):
      all_ys = [key.y for key in self.keys() if key.x == x]
      self.height[x] = (min(all_ys),max(all_ys))
    self.position = P(self.width[1][0],1)

  def __getitem__(self,key):
    if key == self.position:
      return POSITION
    try:
      return self.data[key]
    except KeyError:
      return " "

  def turn(self,direction):
    self.facing += 1 if direction == "R" else -1
    self.facing = self.facing % 4

  def step(self):
    test_pos = self.position + DIRECTIONS[self.facing]
    if not test_pos in self.keys():
      x,y = test_pos
      if self.facing in [0,2]:
        # horizontal
        min,max = self.width[y]
        test_pos = P(min if x > max else max if x < min else x,y)
      else:
        # vertical
        min,max = self.height[x]
        test_pos = P(x,min if y > max else max if y < min else y)
    if self[test_pos] != WALL:
      self[self.position] = TRACES[self.facing]
      self.position = test_pos
      return True
    else:
      return False

  def move(self,distance):
    for _ in range(distance):
      if not self.step():
        break
  def __repr__(self):
    lines = []
    ymax = max(h[1] for h in self.height.values())
    for y in range(1,ymax+1):
      lines.append("".join(self[P(x,y)] for x in range(1,self.width[y][1]+1)))
    return "\n".join(lines)
        

def parse_path(description):
  return [(is_numeric,list(value)) for is_numeric,value in groupby(description[0].strip(),str.isnumeric)]

def part1(board,path):
  for is_numeric,value in path:
    if is_numeric:
      board.move(int("".join(value)))
    else:
      board.turn(value[0])
  return 1000 * board.position.y + 4 * board.position.x + board.facing

def main():
  board,path = split_at(fileinput.input(),is_blank)

  board = Board(board)
  path = parse_path(path)
  print(board)

  print(part1(board,path))
  print(board)
  
if __name__ == "__main__":
  main()
