#!/usr/bin/python3

import fileinput
import re
from more_itertools import split_at

MONKEY = re.compile("Monkey \d+:")
ITEMS = re.compile("  Starting items: ([\d, ]+)")
OPERATION = re.compile("  Operation: new = (.*)\n")
TEST = re.compile("  Test: divisible by (\d+)")
THROW = re.compile("    If (true|false): throw to monkey (\d+)")

ALLOWED_TOKENS = ["old","+","-","*","/"]

def is_blank(line):
  return line.strip() == ""

class Monkey:
  def __init__(self,number):
    self.number = number
    self.activity = 0
    self.items = []
    self.operation = None
    self.test = None
    self.receivers = {}

  def set_test(self,divisor):
    self.test = lambda x: x % divisor == 0
  
  def catch(self,item):
    self.items.append(item)

  def inspect_and_throw(self,cool_down = True):
    self.activity += len(self.items)
    for item in self.items:
      item = self.operation(item)
      if cool_down:
        item = item // 3
      self.receivers[self.test(item)].catch(item)
    self.items = []

  def __lt__(self,other):
    return self.activity < other.activity

  def __repr__(self):
    return "Monkey (activity {}) carrying {} items {}".format(self.activity,len(self.items),self.items)

def read_monkeys():
  data = list(split_at(fileinput.input(),is_blank))
  monkeys = [Monkey(i) for i in range(len(data))]

  for monkey,description in zip(monkeys,data):
    for line in description:
      if MONKEY.match(line):
        pass
      elif ITEMS.match(line):
        items = ITEMS.match(line)
        monkey.items = list(map(int,items.group(1).split(", ")))
      elif OPERATION.match(line):
        tokens = OPERATION.match(line).group(1).split()
        assert(all(token.isnumeric() or token in ALLOWED_TOKENS for token in tokens))
        function = "lambda old: " + " ".join(tokens)
        monkey.operation = eval(function)
      elif TEST.match(line):
        monkey.set_test(int(TEST.match(line).group(1)))
      elif THROW.match(line):
        condition,receiver = THROW.match(line).groups()
        monkey.receivers[condition == "true"] = monkeys[int(receiver)]
      else:
        raise ValueError

  return monkeys

def print_monkeys(monkeys):
  for monkey in monkeys:
    print(monkey)

def run_part(monkeys,number_of_rounds=20,show=1,cool_down=True):
  for i in range(number_of_rounds):
    for monkey in monkeys:
      monkey.inspect_and_throw(cool_down=cool_down)
    if show == 1:
      print("\nAfter round {}:".format(i+1))
      print_monkeys(monkeys)
    elif (i+1) % show == 0:
      print("Round {} finished".format(i+1))
  second,first = sorted(monkeys)[-2:]
  return first.activity * second.activity

def part1(monkeys):
  return run_part(monkeys)

def part2(monkeys):
  return run_part(monkeys,number_of_rounds=10000-20,show=200,cool_down=False)

def main():
  monkeys = read_monkeys()
  print_monkeys(monkeys)

  print("\n",part1(monkeys))
  print("\n",part2(monkeys))

if __name__ == "__main__":
  main()
