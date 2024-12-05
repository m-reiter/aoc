#!/usr/bin/python3

import fileinput
from more_itertools import split_at, partition
from functools import cmp_to_key

def is_blank(line):
  return not(line.strip())

def get_input():
  rules, updates = split_at(fileinput.input(), is_blank)

  rules = [tuple(map(int, rule.split("|"))) for rule in rules]
  updates = [tuple(map(int, update.split(","))) for update in updates]

  return rules, updates

def is_valid(update, rules):
  for rule in rules:
    if len(match := tuple(x for x in update if x in rule)) == 2 and rule != match:
      return False
  return True

def get_middle(update):
  if (l := len(update)) % 2 != 1:
    raise(ValueError("Even number of elements, no middle defined."))
  return update[l // 2]

def cmp(a, b, rules):
  if (a,b) in rules:
    return -1
  if (b,a) in rules:
    return 1
  return 0

def main():
  rules, updates = get_input()

  invalid, valid = partition(lambda x: is_valid(x, rules), updates)

  # part 1
  print(sum(map(get_middle, valid)))

  # part 2
  corrected = [sorted(update, key = cmp_to_key(lambda a,b: cmp(a, b, rules))) for update in invalid]
  print(sum(map(get_middle, corrected)))


if __name__ == "__main__":
  main()
