#!/usr/bin/python3

import fileinput
from itertools import combinations
from functools import reduce
from operator import mul

def balance(weights, ngroups):
  target_weight, remainder = divmod(sum(weights), ngroups)
  assert remainder == 0

  for i in range(1, len(weights)):
    combis = [ set(c) for c in combinations(weights, i) if sum(c) == target_weight ]
    if combis and ngroups == 2:
      return combis
    valid_combis = []
    for combi in combis:
      remainder = weights - combi
      if balance(remainder, ngroups - 1):
        valid_combis.append(combi)
    if valid_combis:
      return valid_combis
  
def main():
  weights = set(map(int, fileinput.input()))

  # part 1
  valid_combis = balance(weights, 3)
  entanglements = [ reduce(mul, combi) for combi in valid_combis ]
  print(min(entanglements))

  # part 2
  valid_combis = balance(weights, 4)
  entanglements = [ reduce(mul, combi) for combi in valid_combis ]
  print(min(entanglements))

if __name__ == "__main__":
  main()
