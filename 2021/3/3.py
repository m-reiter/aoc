#!/usr/bin/python3

import fileinput

def read_data():
  return [list(map(int, line.strip())) for line in fileinput.input()]

def part1(report):
  number = len(report)
  frequencies = list(map(sum,zip(*report)))
  gamma = int("".join(["0" if f < number / 2 else "1" for f in frequencies]),2)
  epsilon = int("".join(["0" if f > number / 2 else "1" for f in frequencies]),2)
  return gamma*epsilon

def main():
  report = read_data()
  print(part1(report))

if __name__ == "__main__":
  main()
