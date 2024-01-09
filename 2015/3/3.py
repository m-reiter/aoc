#!/usr/bin/python3

import fileinput
from more_itertools import chunked

from P import P

DIRECTIONS = {
  "^": P(0,-1),
  "v": P(0,1),
  "<": P(-1,0),
  ">": P(1,0)
}

def main():
  path = fileinput.input().readline().strip()
  
  position = P(0,0)
  houses = { position }

  for direction in path:
    position += DIRECTIONS[direction]
    houses.add(position)

  print(len(houses))

  santa = robo = P(0,0)
  houses = { santa }

  for ds,dr in chunked(path,2):
    santa += DIRECTIONS[ds]
    robo += DIRECTIONS[dr]
    houses.add(santa)
    houses.add(robo)

  print(len(houses))

if __name__ == "__main__":
  main()
