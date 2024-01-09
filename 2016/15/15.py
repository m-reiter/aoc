#!/usr/bin/python3

import fileinput
import re

DISC = re.compile("Disc #(\d+) has (\d+) positions; at time=0, it is at position (\d+).")

def find_earliest(discs):
  earliest = 0
  step = 1
  for disc in discs:
    position,count,start = map(int,disc)
    while (earliest+position-(count-start)) % count != 0:
      earliest += step
    step *= count
  return earliest

def main():
  discs = [ DISC.match(line).groups() for line in fileinput.input() ]
  print(find_earliest(discs))
  discs.append((len(discs)+1,11,0))
  print(find_earliest(discs))

if __name__ == "__main__":
  main()
