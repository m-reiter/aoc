#!/usr/bin/python3

import fileinput
import re

from collections import defaultdict

COORDS = re.compile(".* (\\d+),(\\d+) through (\\d+),(\\d+)")

ON = lambda x: True
OFF = lambda x: False
TOGGLE = lambda x: not x

def main():
  instructions = [ line.strip() for line in fileinput.input() ]

  lights = defaultdict(lambda: defaultdict(bool))
  brightness = defaultdict(lambda: defaultdict(int))

  for instruction in instructions:
    x1,y1,x2,y2 = map(int,COORDS.match(instruction).groups())
    if instruction.startswith("toggle"):
      func = TOGGLE
      addition = 2
    elif instruction.startswith("turn on"):
      func = ON
      addition = 1
    elif instruction.startswith("turn off"):
      func = OFF
      addition = -1
    else:
      raise ValueError

    # part 1
    for x in range(x1,x2+1):
      for y in range(y1,y2+1):
        lights[x][y] = func(lights[x][y])
        brightness[x][y] = max(brightness[x][y]+addition,0)

  print(sum(sum(column.values()) for column in lights.values()))
  print(sum(sum(column.values()) for column in brightness.values()))

if __name__ == "__main__":
  main()
