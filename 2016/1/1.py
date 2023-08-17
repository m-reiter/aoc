#!/usr/bin/python3

import fileinput
from P import P

STEPS = [ P(0,1), P(1,0), P(0,-1), P(-1,0)]
TURNS = { 'R': 1, 'L': -1 }

def walk_path(path, start=P(0,0), heading=0, break_on_revisit=False):
  position = start
  visited = { start }
  for instruction in path.split(", "):
    heading += TURNS[instruction[0]]
    heading = heading % len(STEPS)
    for _ in range(int(instruction[1:])):
      position += STEPS[heading]
      if position in visited and break_on_revisit:
        return position
      visited.add(position)
  return position

def main():
  path = fileinput.input().readline()
  end_point = walk_path(path)
  print("part1: ",sum(map(abs,end_point)))
  end_point = walk_path(path,break_on_revisit=True)
  print("part2: ",sum(map(abs,end_point)))

if __name__ == "__main__":
  main()
