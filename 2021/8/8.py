#!/usr/bin/python3

import fileinput

DIGITS = {
  "abcefg": 0,
  "cf": 1,
  "acdeg": 2,
  "acdfg": 3,
  "bcdf": 4,
  "abdfg": 5,
  "abdefg": 6,
  "acf": 7,
  "abcdefg": 8,
  "abcdfg": 9
}

def calc_hashes(combinations=DIGITS.keys(), reverse=False):
  lookuptable = {}
  for letter in "abcdefg":
    shortest = min(len(x) for x in combinations if letter in x)
    count = len([ x for x in combinations if letter in x])
    if reverse:
      lookuptable[letter] = (count,shortest)
    else:
      lookuptable[(count,shortest)] = letter
  return lookuptable 

def get_display(lookuptable,data):
  display = []
  for line in data:
    combinations,digits = line.strip().split(" | ")
    translation_table = calc_hashes(combinations.split(), reverse=True)
    line = [ DIGITS["".join(sorted(lookuptable[translation_table[x]] for x in digit))] for digit in digits.split() ]
    display.append(line)
  return display

def part1(display):
  count  = 0
  for line in display:
    count += sum(1 for x in line if x in [1,4,7,8]) 
  return count

def part2(display):
  return sum(map(int,["".join(map(str,line)) for line in display]))

def main():
  lookuptable = calc_hashes()

  data = list(fileinput.input())
  display = get_display(lookuptable,data)

  print(part1(display))
  print(display)
  print(part2(display))

if __name__ == "__main__":
  main()
