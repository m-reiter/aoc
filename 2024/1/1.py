#!/usr/bin/python3

import fileinput
from more_itertools import unzip
from collections import Counter

def get_input():
  return [list(inputlist) for inputlist in unzip([list(map(int,line.split())) for line in fileinput.input()])]

def main():
  inputlists = get_input()

  # part 1
  print(sum(abs(a-b) for a,b in zip(*[sorted(list) for list in inputlists])))

  # part 2
  count_left, count_right = map(Counter, inputlists)
  print(sum(key * value * count_right[key] for key, value in count_left.items()))

if __name__ == "__main__":
  main()
