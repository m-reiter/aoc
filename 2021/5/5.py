#!/usr/bin/python3

import fileinput
from collections import defaultdict
from numpy import sign

def read_input():
  return [[tuple(map(int,segment.split(","))) for segment in line.split(" -> ")] for line in fileinput.input()]

def sum_field(field, threshold):
  return sum([sum( 1 for space in column.values() if space >= threshold) for column in field.values()])

def part1(lines):
  field = defaultdict(lambda: defaultdict(int))
  unhandled = []
  for line in lines:
    (x1,y1),(x2,y2) = line
    if x1 == x2:
      y1,y2 = sorted([y1,y2])
      for y in range(y1,y2+1):
        field[x1][y] += 1
    elif y1 == y2:
      x1,x2 = sorted([x1,x2])
      for x in range(x1,x2+1):
        field[x][y1] += 1
    else:
      unhandled.append(line)
  sum = sum_field(field,2)
  return sum,field,unhandled

def part2(field,lines):
  for (x1,y1),(x2,y2) in lines:
    step_x = sign(x2-x1)
    step_y = sign(y2-y1)
    for x in range(x1,x2+step_x,step_x):
      field[x][y1+(x-x1)*step_x*step_y] += 1
  return sum_field(field,2)

def main():
   lines = read_input()
   safe1,field,unhandled = part1(lines)
   print(safe1)
   print(part2(field,unhandled))

if __name__ == "__main__":
  main()
