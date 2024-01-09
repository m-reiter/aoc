#!/usr/bin/python3

import fileinput
import re

from itertools import cycle
from functools import reduce
from math import gcd

DIRECTIONS = "LR"

NODE = re.compile("(\w{3}) = \((\w{3}), (\w{3})\)")

def read_input():
  with fileinput.input() as f:
    instructions = [ DIRECTIONS.index(c) for c in f.readline().strip() ]

    f.readline()

    desert_map = {}
    for line in f:
      source, *target = NODE.match(line).groups()
      desert_map[source] = target

    return instructions, desert_map

def cycle_iterator(states, hits, state):
  offset = states.index(state)
  print(offset)
  length = len(states) - offset
  initial = set(hit for hit in hits if hit < offset)
  hits = [ hit for hit in hits if hit >= offset ]
  print(hits, length)

  yield initial

  cycles = 0

  while True:
    yield set(cycles * length + hit for hit in hits)
    cycles += 1

def find_period(states, hits, state):
  offset = states.index(state)
  length = len(states) - offset
  initial = set(hit for hit in hits if hit < offset)
  assert not initial
  hits = [ hit for hit in hits if hit >= offset ]
  return min(hits)
  assert len(hits) == 1
  assert length == hits[0]
  return length 

def find_cycle(start, instructions, desert_map):
  previous = []
  hits = []
  position = start

  for step, direction in enumerate(cycle(instructions), 1):
    position = desert_map[position][direction]
    if position[-1] == "Z":
      return step
    
  for move, (index, direction) in enumerate(cycle(enumerate(instructions))):
    if (position, index) in previous:
      break
    previous.append((position, index))
    if position[-1] == "Z":
      hits.append(move)
    position = desert_map[position][direction]

  return find_period(previous, hits, (position, index))

def lcm(a, b):
  return abs(a * b) // gcd(a, b)

def main():
  instructions, desert_map = read_input()

  # part 1
  path = cycle(instructions)
  position = "AAA"

  if position in desert_map:
    for step, direction in enumerate(path, 1):
      position = desert_map[position][direction]

      if position == "ZZZ":
        break

    print(step)

  # part 2
  starts = [ pos for pos in desert_map if pos[-1] == "A" ]
  print(starts)
  cycles = [ find_cycle(start, instructions, desert_map) for start in starts ]
  print(cycles)
  least = reduce(lcm, cycles)
  print([ least // cycle for cycle in cycles ])
  print(least)

  return
  print(cycles)
  hits = [ set() for _ in starts ]
  print(hits)

  for new in zip(*cycles):
    hits = [ hit.union(additional) for hit, additional in zip (hits, new) ]
    print(hits)
    if len(hits[0]) == 2:
      break
    common = reduce(set.intersection, hits)
    if common:
      break

  print(min(common))
  
if __name__ == "__main__":
  pass
  main()
