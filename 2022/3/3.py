#!/usr/bin/python3

import fileinput
from more_itertools import divide, chunked

def read_input():
  return [list(map(list,divide(2,line.strip()))) for line in fileinput.input()]
  
def get_priority(item):
  offset = 38 if item.isupper() else 96
  return ord(item)-offset

def part1(rucksacks):
  return sum(get_priority(set(a).intersection(set(b)).pop()) for a,b in rucksacks)

def part2(rucksacks):
  sum = 0
  for group in chunked(rucksacks, 3):
    #items = set.intersection(*[set(a + b) for a,b in rucksacks]) 
    items = [set(a + b) for a,b in group]
    sum += get_priority(set.intersection(*items).pop())
  return sum

def main():
  rucksacks = read_input()
  print(part1(rucksacks))
  print(part2(rucksacks))

if __name__ == "__main__":
  main()
