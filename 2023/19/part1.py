#!/usr/bin/python3

import fileinput
import attr
import operator
import re

from more_itertools import split_at
from itertools import product

WORKFLOW = re.compile("(\w+){([^}]+)}")
PART = re.compile("{x=(\d+),m=(\d+),a=(\d+),s=(\d+)}")

COMPARISONS = { "<": operator.lt, ">": operator.gt }

IN = "in"
ACCEPT = "A"
REJECT = "R"

def is_blank(line):
  return not line.strip()

@attr.s
class Part:
  x = attr.ib()
  m = attr.ib()
  a = attr.ib()
  s = attr.ib()

  @classmethod
  def from_line(cls, line):
    return cls(*map(int, PART.match(line).groups()))

  @property
  def rating(self):
    return sum(getattr(self, char) for char in "xmas")

  def __radd__(self, other):
    return other + self.rating

@attr.s
class Rule:
  category = attr.ib()
  comparator = attr.ib()
  value = attr.ib()
  
  @classmethod
  def from_string(cls, string):
    category, comparator, *value = string
    
    return cls(category, comparator, int("".join(value)))

  def match(self, part):
    return COMPARISONS[self.comparator](getattr(part, self.category), self.value)

@attr.s
class Workflow:
  default = attr.ib()
  rules = attr.ib(factory = list)

  @classmethod
  def from_rules(cls, rules):
    *rules, default = rules.split(",")

    workflow = cls(default)

    for rule in rules:
      string, result = rule.split(":")

      workflow.rules.append((Rule.from_string(string), result))

    return workflow

  def handle(self, part):
    for rule, result in self.rules:
      if rule.match(part):
        return result
    return self.default

class Ruleset(dict):
  def accept(self, part, verbose = True):
    current = IN

    if verbose:
      print("{}: ".format(part), end = "")

    while True:
      if verbose:
        print("{} -> ".format(current), end = "")

      current = self[current].handle(part)

      if current in (ACCEPT, REJECT):
        if verbose:
          print(current)

        return current == ACCEPT

def read_input():
  workflows, parts = split_at(fileinput.input(), is_blank)

  ruleset = Ruleset()

  for workflow in workflows:
    name, rules = WORKFLOW.match(workflow).groups()
    ruleset[name] = Workflow.from_rules(rules)

  parts = [ Part.from_line(part) for part in parts ]

  return ruleset, parts

def main():
  ruleset, parts = read_input()

  # part 1
  accepted = [ part for part in parts if ruleset.accept(part) ]

  print(sum(accepted))

  # part 2
  print(sum(ruleset.accept(Part(*values), verbose = False) for values in product(range(1,4001), repeat = 4)))

if __name__ == "__main__":
  main()
