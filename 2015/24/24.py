#!/usr/bin/python3

import fileinput
from itertools import combinations
from functools import reduce
from operator import mul

def balance(weights, ngroups):
  pass
  
def main():
  weights = set(map(int, fileinput.input()))
  target_weight, remainder = divmod(sum(weights), 3)
  assert remainder == 0

  for i in range(len(weights)):
    combis = [ set(c) for c in combinations(weights, i) if sum(c) == target_weight ]
    valid_combis = []
    for combi in combis:
      remainder = weights - combi
      for j in range(len(remainder)):
        seconds = [ set(c) for c in combinations(remainder, j) if sum(c) == target_weight ]
        if seconds:
          valid_combis.append(combi)
          break
    if valid_combis:
      break

  entanglements = [ reduce(mul, combi) for combi in valid_combis ]
  print(min(entanglements))

if __name__ == "__main__":
  main()
