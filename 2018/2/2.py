#!/usr/bin/python3

import fileinput
from collections import Counter
from itertools import combinations

def main():
  IDs = [line.strip() for line in fileinput.input()]
  twos = [ID for ID in IDs if 2 in Counter(ID).values()]
  threes = [ID for ID in IDs if 3 in Counter(ID).values()]

  print(len(twos)*len(threes))

  for x,y in combinations(IDs,2):
    if sum(a != b for a,b in zip(x,y)) == 1:
      break

  for i,letter in enumerate(x):
    if y[i] != letter:
      break

  print(x)
  print(y)
  print(x[:i]+x[i+1:])

if __name__ == "__main__":
  main()
