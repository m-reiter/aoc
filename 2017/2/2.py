#!/usr/bin/python3

import fileinput
from itertools import permutations

def read_input():
  return [list(map(int, line.split())) for line in fileinput.input()]

def part1(spreadsheet):
  return sum(max(line)-min(line) for line in spreadsheet)

def find_quotient(line):
  for x,y in permutations(line,2):
    if x % y == 0:
      return x // y

def part2(spreadsheet):
  return sum(find_quotient(line) for line in spreadsheet)

def main():
  spreadsheet = read_input()
  print(part1(spreadsheet))
  print(part2(spreadsheet))

if __name__ == "__main__":
  main()
