#!/usr/bin/python3

INPUT = 361527
TEST = [1, 12, 23, 1024]

from P import P
from collections import defaultdict

def position(field):
  odd = 1
  while odd*odd <= field:
    odd += 2
  odd -= 2
  position = P((odd-1)//2,-(odd-1)//2)
  steps = field - odd*odd
  if steps:
    # 1 to the right
    position += P(1,0)
    steps -= 1
  if steps:
    # upwards
    up = min(steps,odd)
    position += up*P(0,1)
    steps -= up
  if steps:
    # left
    left = min(steps,odd+1)
    position += left*P(-1,0)
    steps -= left
  if steps:
    # down
    down = min(steps,odd+1)
    position += down*P(0,-1)
    steps -= down
  if steps:
    # right
    position += steps*P(1,0)
  return position

def distance(field):
  return sum(map(abs,position(field)))

def part2():
  values = defaultdict(int)
  values[P(0,0)] = 1
  field = 1
  while True:
    field += 1
    p = position(field)
    new_value = sum(values[q] for q in p.get_neighbors())
    if new_value > INPUT:
      return new_value
    values[p] = new_value

def main():
  print(distance(INPUT))
  print(part2())

if __name__ == "__main__":
  main()
