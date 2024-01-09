#!/usr/bin/python3

import fileinput

from collections import Counter, defaultdict
from more_itertools import chunked

MFCSAM = Counter({ k.rstrip(":"): int(v) for k, v in chunked(
  """children: 3
  cats: 7
  samoyeds: 2
  pomeranians: 3
  akitas: 0
  vizslas: 0
  goldfish: 5
  trees: 3
  cars: 2
  perfumes: 1""".split(), 2) })

def read_input():
  return [
    Counter({ mapping.split(": ")[0]: int(mapping.split(": ")[1]) for mapping in line.strip().split(": ", 1)[1].split(", ") })
    for line in fileinput.input()
  ]
  sues = []
  for line in fileinput.input():
    sue = Counter({ mapping.split(": ")[0]: int(mapping.split(": ")[1]) for mapping in line.strip().split(": ", 1)[1].split(", ") })
    print(sue)

def main():
  sues = read_input()

  # part 1
  print([ number for number, sue in enumerate(sues, 1) if all(value == MFCSAM[key] for key, value in sue.items()) ][0])

  # part 2
  ranges = defaultdict(lambda: int.__eq__)
  ranges.update({
    "cats": int.__gt__,
    "trees": int.__gt__,
    "pomeranians": int.__lt__,
    "goldfish": int.__lt__
  })

  print([ number for number, sue in enumerate(sues, 1) if all(ranges[key](value, MFCSAM[key]) for key, value in sue.items()) ][0])

if __name__ == "__main__":
  main()
