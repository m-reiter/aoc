#!/usr/bin/python3

import fileinput
import re

from collections import defaultdict
from functools import reduce

def read_input():
  replacements = defaultdict(set)

  for line in fileinput.input():
    if "=>" in line:
      source, product = line.strip().split(" => ")
      replacements[source].add(product)
    elif line:
      molecule = line.strip()

  return molecule, replacements

def get_products(molecule, replacements):
  products = set()

  for source, subs in replacements.items():
    for m in re.finditer(source, molecule):
      products.update(molecule[:m.start()] + sub + molecule[m.end():] for sub in subs if len(sub) < m.end() - m.start() )

  return products

def main():
  molecule, replacements = read_input()

  # part 1
  print(len(get_products(molecule, replacements)))

  # part 2
  print(len(molecule))
  reverse = defaultdict(set)
  for source, targets in replacements.items():
    for target in targets:
      reverse[target].add(source)
  states = { molecule }
  steps = 0
  while True:
    steps += 1
#    new_states = set()
#    for state in states:
#      new = get_products(state, replacements)
#      new_states.update(new)
#      replacements[state].update(new)
#    states.update(new_states)

    states = reduce(set.union, [ get_products(state, reverse) for state in states ])
    print(steps, len(states), min(len(x) for x in states))
    
    if "e" in states:
      break

  print(steps)

if __name__ == "__main__":
  main()
