#!/usr/bin/python3

import hashlib
from collections import defaultdict

from P import P

DIRECTIONS = [ ('U',P(0,-1)),('D',P(0,1)),('L',P(-1,0)),('R',P(1,0)) ]
CODE = 'rrrbmfta'

def is_open(door,hexhash):
  return hexhash[door] in "bcdef"

def step(state):
  new_state = defaultdict(list)
  for position,paths in state.items():
    neighbors = position.get_neighbors(diagonals=False, borders=P(3,3))
    for path in paths:
      hexhash = hashlib.md5((CODE+path).encode()).hexdigest()
      for door in range(4):
        new_position = position + DIRECTIONS[door][1]
        if is_open(door,hexhash) and new_position in neighbors:
          new_state[new_position].append(path + DIRECTIONS[door][0])
  return new_state

def part1():
  state = { P(0,0): [''] }
  while state and P(3,3) not in state:
    state = step(state)
    print(state)
  print(state[P(3,3)][0])

def part2():
  state = { P(0,0): [''] }
  while state:
    state = step(state)
    if P(3,3) in state:
      longest = state[P(3,3)][0]
      state.pop(P(3,3))
  print(len(longest))

def main():
  part1()
  part2()

if __name__ == "__main__":
  main()
