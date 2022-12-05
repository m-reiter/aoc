#!/usr/bin/python3

import fileinput

def read_input():
  assignments = []
  for line in fileinput.input():
     ranges = [map(int,range.split("-")) for range in line.strip().split(",")]
     assignments.append([set(range(min,max+1)) for min,max in ranges])
  return assignments

def part1(assignments):
  return sum(a.issubset(b) or b.issubset(a) for a,b in assignments)
  
def part2(assignments):
  return sum(len(a & b) > 0 for a,b in assignments)
  
def main():
  assignments = read_input()
  print(part1(assignments))
  print(part2(assignments))

if __name__ == "__main__":
  main()
