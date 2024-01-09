#!/usr/bin/python3

import fileinput
import attr
import operator
import re

from more_itertools import split_at
from itertools import product
from collections import UserDict

XMAS = "xmas"

WORKFLOW = re.compile("(\w+){([^}]+)}")
PART = re.compile("{x=(\d+),m=(\d+),a=(\d+),s=(\d+)}")

COMPARISONS = { "<": operator.lt, ">": operator.gt }

IN = "in"
ACCEPT = "A"
REJECT = "R"

def is_blank(line):
  return not line.strip()

@attr.s(these = { char: attr.ib(converter = int) for char in XMAS })
class Part:
  @classmethod
  def from_line(cls, line):
    return cls(*PART.match(line).groups())

  @property
  def rating(self):
    return sum(getattr(self, char) for char in XMAS)

  def __radd__(self, other):
    return other + self.rating

@attr.s
class Rule:
  category = attr.ib()
  comparator = attr.ib()
  value = attr.ib(converter = int)
  
  @classmethod
  def from_string(cls, string):
    category, comparator, *value = string
    
    return cls(category, comparator, "".join(value))

  def match(self, part):
    return COMPARISONS[self.comparator](getattr(part, self.category), self.value)

  def to_ranges(self):
    if self.comparator == ">":
      return Range(self.value + 1, 4000), Range(1, self.value)
    else:
      return Range(1, self.value - 1), Range(self.value, 4000)

@attr.s
class Range:
  first = attr.ib(default = 1)
  last = attr.ib(default = 4000)

  def combine(self, other):
    return Range(max(self.first, other.first), min(self.last, other.last))

  @property
  def count(self):
    return max(0, self.last - self.first + 1)

  def __contains__(self, number):
    return self.first <= number <= self.last

@attr.s(these = { char: attr.ib(factory = Range) for char in XMAS })
class Filter:
  def __contains__(self, part):
    return all(getattr(part, char) in getattr(self, char) for char in XMAS)

  def split(self, rule):
    ranges = rule.to_ranges()

    split = tuple(attr.evolve(self) for _ in ranges)

    for f, r in zip(split, ranges):
      setattr(f, rule.category, getattr(self, rule.category).combine(r))

    return split

  @property
  def count(self):
    return self.x.count * self.m.count * self.a.count * self.s.count
  
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

  def evolve(self, filter):
    results = []

    for rule, result in self.rules:
      match, fail = filter.split(rule)
      results.append((match, result))
      filter = fail

    results.append((fail, self.default))

    return results

@attr.s
class Ruleset(UserDict):
  data = attr.ib(factory = dict)
  accepts = attr.ib(factory = list)

  def accept(self, part, verbose = True):
    if self.accepts and not verbose:
      return any(part in filter for filter in self.accepts)

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

  def analyse(self):
    states = [ (Filter(), IN) ]

    while states:
      filter, rule = states.pop(0)
      for new_filter, new_rule in self[rule].evolve(filter):
        if new_rule == ACCEPT:
          self.accepts.append(new_filter)
        elif new_rule != REJECT:
          states.append((new_filter, new_rule))

def read_input():
  workflows, parts = split_at(fileinput.input(), is_blank)

  ruleset = Ruleset()

  for workflow in workflows:
    name, rules = WORKFLOW.match(workflow).groups()
    ruleset[name] = Workflow.from_rules(rules)

  ruleset.analyse()

  parts = [ Part.from_line(part) for part in parts ]

  return ruleset, parts

def main():
  ruleset, parts = read_input()

  verbose = len(parts) < 10

  # part 1
  accepted = [ part for part in parts if ruleset.accept(part, verbose = verbose) ]

  print(sum(accepted))

  # part 2
  print(sum(filter.count for filter in ruleset.accepts))

if __name__ == "__main__":
  main()
