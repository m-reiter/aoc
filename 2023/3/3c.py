#!/usr/bin/python3

import fileinput
import re

from functools import reduce
from operator import mul

NUMBER = re.compile("\d+")
SYMBOL = re.compile("[^\d\.]")
GEAR_SYMBOL = "*"

class Number():
  def __init__(self,x,y,value):
    self.value = int(value)
    self.x = x
    self.y = y
    self.length = len(value)
    self.adjacent_parts = []

  def __repr__(self):
    return "Number {} at {} spanning {} spaces".format(self.value, (self.x,self.y), self.length) 

  def __contains__(self, position):
    return self.x-1 <= position.x <= self.x+self.length and self.y-1 <= position.y <= self.y+1

  def is_part_number(self):
    return bool(self.adjacent_parts)

class Part():
  def __init__(self,x,y,symbol):
    self.x = x
    self.y = y
    self.symbol = symbol
    self.adjacent_numbers = []

  def __repr__(self):
    return "Part '{}' at {}".format(self.symbol, (self.x,self.y))

  def is_gear(self):
    return self.symbol == GEAR_SYMBOL and len(self.adjacent_numbers) == 2

  def gear_ratio(self):
    if self.is_gear():
      return reduce(mul, self.adjacent_numbers)
    return 0

def read_input():
  parts = []
  numbers = []

  for y, line in enumerate(fileinput.input()):
    line = line.strip()
    for part in SYMBOL.finditer(line):
      x = part.start()
      parts.append(Part(x,y,part.group(0)))
    for number in NUMBER.finditer(line):
      x = number.start()
      numbers.append(Number(x,y,number.group(0)))

  return parts, numbers

def set_neighbors(parts, numbers):
  for part in parts:
    for number in numbers:
      if part in number:
        part.adjacent_numbers.append(number.value)
        number.adjacent_parts.append(part)
    
def main():
  parts, numbers = read_input()
  
  set_neighbors(parts, numbers)

  # part 1
  part_numbers = [ number.value for number in numbers if number.is_part_number() ]
  print(sum(part_numbers))

  # part 2
  gear_ratios = [ part.gear_ratio() for part in parts ]

  print(sum(gear_ratios))

if __name__ == "__main__":
  main()
