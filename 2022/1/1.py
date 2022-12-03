#!/usr/bin/python3

import fileinput

class Elf:
  
  def __init__(self, items):
    self.items = map(int,items)
    self.calories = sum(self.items)
    self.number_of_items = len(items)

  def __repr__(self):
    return "Elf with %s food items (%s calories)" % (self.number_of_items, self.calories)

def read_input():
  elves = []
  calories = []
  for line in fileinput.input():
    line = line.strip()
    if line:
      calories.append(line)
    else:
      elves.append(Elf(calories))
      calories = []
  elves.append(Elf(calories))
  return elves

def part1(elves):
  return max(elf.calories for elf in elves)

def part2(elves):
  return sum(sorted([elf.calories for elf in elves], reverse = True)[:3])

def main():
  elves = read_input()
  print(part1(elves))
  print(part2(elves))

if __name__ == "__main__":
  main()
