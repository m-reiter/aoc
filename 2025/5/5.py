#!/usr/bin/python3

import fileinput
from more_itertools import split_at

def is_blank(line):
  return not line.strip()

def main():
  ranges, ingredients = split_at(fileinput.input(), is_blank)
  fresh_ranges = set()
  for r in ranges:
    start, stop = map(int, r.split("-"))
    fresh_ranges.add(range(start, stop + 1))
  ingredients = list(map(int, ingredients))

  # consolidate ranges
  consolidated = { fresh_ranges.pop() }
  for r in fresh_ranges:
    overlapping = { o for o in consolidated if r.start <= o.stop and r.stop >= o.start }
    consolidated -= overlapping
    overlapping.add(r)
    consolidated.add(range(min(o.start for o in overlapping), max(o.stop for o in overlapping)))

  # part 1
  print(sum(any(i in r for r in consolidated) for i in ingredients))

  # part 2
  print(sum(len(r) for r in consolidated))

if __name__ == "__main__":
  main()
