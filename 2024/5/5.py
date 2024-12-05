#!/usr/bin/python3

import fileinput
from more_itertools import split_at

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

def main():
  rules, updates = get_input()

  # part 1
  print(sum(map(get_middle, [update for update in updates if is_valid(update, rules)])))

if __name__ == "__main__":
  main()
