#!/usr/bin/python3

import fileinput

class TicketData:

  def __init__(self, input_):

    self.rules = {}
    self.nearby = []
    
    mode = 0

    for line in input_:

      line = line.strip()

      if not line:
        
        mode += 1

      elif mode == 0:

        field, rules = line.split(": ")

        ranges = [[int(x) for x in rule.split("-")] for rule in rules.split(" or ")]

        self.rules[field] = ranges

      elif mode == 1:

        if not line.startswith("your ticket:"):

          self.own = [int(i) for i in line.split(",")]

      else:

        if not line.startswith("nearby tickets:"):

          self.nearby.append([int(i) for i in line.split(",")])

  def validate_for_rule(self, number, rule):

    valid = False

    for min,max in self.rules[rule]:
      if min <= number <= max:
        valid = True

    return valid
  
  def validate_for_any(self, number):

    valid = False

    for rule in self.rules:
      if self.validate_for_rule(number, rule):
        valid = True

    return valid
  
  def solve_part1(self):

    return sum([number for numbers in self.nearby for number in numbers if not self.validate_for_any(number)])

  def remove_invalids(self):

    valids = []

    for ticket in self.nearby:

      if all([self.validate_for_any(number) for number in ticket]):

        valids.append(ticket)

    self.nearby = valids

  def check_valid_columns(self):

    valid_columns = {}

    for rule in self.rules:

      valid = []
    
      for i in range(len(self.own)):

        if all([self.validate_for_rule(ticket[i], rule) for ticket in self.nearby]):

          valid.append(i)

      valid_columns[rule] = valid

    return valid_columns

  def calculate_mapping(self):

    self.remove_invalids()

    valid_columns = self.check_valid_columns()

    self.mapping = {}

    while len(valid_columns) > 0:

      key = min(valid_columns.keys(), key = lambda key: len(valid_columns[key]))
       
      column = valid_columns.pop(key)[0]

      self.mapping[key] = column

      for columns in valid_columns.values():

        columns.remove(column)

  def solve_part2(self):

    self.calculate_mapping()
    
    departures = [key for key in self.rules if key.startswith("departure")]

    solution = 1

    for value in [self.own[self.mapping[key]] for key in departures]:
      solution *= value

    return solution


def main():
  
  data = TicketData(fileinput.input())

  print(data.solve_part1())

  print(data.solve_part2())

if __name__ == "__main__":
  main()
