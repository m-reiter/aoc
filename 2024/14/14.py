#!/usr/bin/python3

import fileinput
import re
from itertools import groupby
from math import prod
from P import P

ROBOT = re.compile("p=(\d+),(\d+) v=(-?\d+),(-?\d+)")

def propagate(robots, size, steps = 1):
  #positions = [ P((start.x + velocity.x * steps) % size.x, (start.y + velocity.y * steps) % size.y) for start, velocity in robots ]
  positions = [ P((end := start + velocity * steps).x % size.x, end.y % size.y) for start, velocity in robots ]
  return positions

def sector(position, size):
  mid_x = (size.x - 1) / 2
  mid_y = (size.y - 1) / 2

  if position.x == mid_x or position.y == mid_y:
    return 0

  return 1 * (position.x < mid_x) + 10 * (position.y < mid_y) + 100

def safety_factor(positions, size):
  key = lambda p: sector(p, size)

  return prod(len(list(robots)) for sector, robots in groupby(sorted(positions, key = key), key = key) if sector != 0)

def print_map(positions, size, skip_middle = True):
  mid_x = (size.x - 1) / 2
  mid_y = (size.y - 1) / 2

#  print("\033[H")
  for y in range(size.y):
    for x in range(size.x):
      print(" " if skip_middle and (x == mid_x or y == mid_y) else str(positions.count(P(x, y)))[-1] if P(x, y) in positions else ".", end = "")
    print()
  print()

def main():
  robots = []
  for line in fileinput.input():
    px, py, vx, vy = map(int, ROBOT.match(line).groups())
    robots.append((P(px, py), P(vx, vy)))

  size = P(11, 7) if len(robots) < 100 else P(101, 103)

  # part 1
  positions = propagate(robots, size, steps = 100)

  print(safety_factor(positions, size = size))

  # part 2
  steps = 0
  mid_x = (size.x - 1) / 2
  while True:
    positions = propagate(robots, size, steps = steps)
    if len(set(positions)) == len(positions):
      print_map(positions, size, skip_middle = False)
      print(steps)
      print()
      break
    steps += 1

if __name__ == "__main__":
  main()
