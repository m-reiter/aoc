#!/usr/bin/python3

import fileinput
from more_itertools import split_at

def is_blank(line):
  return not line.strip()

def main():
  ranges, ingredients = split_at(fileinput.input(), is_blank)
  fresh_ranges = []
  for r in ranges:
    start, stop = map(int, r.split("-"))
    fresh_ranges.append(range(start, stop + 1))
  ingredients = list(map(int, ingredients))

  # part 1
  print(sum(any(i in r for r in fresh_ranges) for i in ingredients))

if __name__ == "__main__":
  main()
