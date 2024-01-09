#!/usr/bin/python3

import fileinput

from itertools import product

TARGET = 150
#TARGET = 25

def main():
  containers = list(map(int, fileinput.input()))

  combinations = [ combo for combo in product((0,1), repeat = len(containers))
                   if sum(present * container for present, container in zip(combo, containers)) == TARGET ]

  # part 1
  print(len(combinations))

  # part 2
  numbers = [ sum(combo) for combo in combinations ]
  least = min(numbers)
  print(numbers.count(least))

if __name__ == "__main__":
  main()
