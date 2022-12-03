#!/usr/bin/python3

import fileinput

VALUES = {
  'A': 1,
  'B': 2,
  'C': 3,
  'X': 1,
  'Y': 2,
  'Z': 3
}

OFFSETS = {
  'X': -1,
  'Y': 0,
  'Z': 1
}

def read_input():
  return [line.strip().split() for line in fileinput.input()]

def get_score(elf, player):
  return (player-VALUES[elf] + 1) % 3 * 3 + player

def get_choice(elf, result):
  return (VALUES[elf] + OFFSETS[result] - 1) % 3 + 1

def part1(strategy):
  return sum(get_score(elf, VALUES[player]) for elf, player in strategy)

def part2(strategy):
  return sum(get_score(elf, get_choice(elf, result)) for elf, result in strategy)

def main():
  strategy = read_input()
  print(part1(strategy))
  print(part2(strategy))

if __name__ == "__main__":
  main()
