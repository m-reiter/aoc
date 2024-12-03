#!/usr/bin/python3

import fileinput
from more_itertools import pairwise

def sign(x):
  return (x > 0) - (x < 0)

def find_fault(line):
  direction = sign(line[-1] - line[0])
  for i,(a,b) in enumerate(pairwise(line)):
    if sign(b - a) != direction or abs(b - a) not in {1,2,3}:
      return i
  return -1

def is_safe(line):
  return find_fault(line) == -1

def is_safe_with_dampener(line):
  if (fault := find_fault(line)) == -1:
    return True
  for offset in (0,1):
    dampened = line.copy()
    dampened.pop(fault + offset)
    if is_safe(dampened):
      return True
  return False

def main():
  inputdata = [list(map(int, line.strip().split())) for line in fileinput.input()]

  # part 1
  print(sum(is_safe(line) for line in inputdata))

  # part 2
  print(sum(is_safe_with_dampener(line) for line in inputdata))

if __name__ == "__main__":
  main()
