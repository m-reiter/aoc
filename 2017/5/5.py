#!/usr/bin/python3

import fileinput

def part1(instructions):
  instructions = instructions.copy()
  position = 0
  steps = 0
  while 0 <= position < len(instructions):
    steps += 1
    offset = instructions[position]
    instructions[position] += 1
    position += offset
  return steps

def part2(instructions):
  instructions = instructions.copy()
  position = 0
  steps = 0
  while 0 <= position < len(instructions):
    steps += 1
    offset = instructions[position]
    instructions[position] += -1 if offset >= 3 else 1
    position += offset
  return steps

def main():
  instructions = [int(line) for line in fileinput.input()]
  print(part1(instructions))
  print(part2(instructions))

if __name__ == "__main__":
  main()
