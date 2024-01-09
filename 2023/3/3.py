#!/usr/bin/python3

import fileinput
import re

from functools import reduce
from operator import mul

from P import P

NUMBER = re.compile("\d+")
SYMBOL = re.compile("[^\d\.]")

class Number(P):
  def __new__(self,x,y,value):
    number = super().__new__(Number,x,y)
    number.value = int(value)
    number.length = len(value)
    return number

  def __repr__(self):
    return "Number {} at {} spanning {} spaces".format(self.value, super().__repr__(), self.length) 

  def get_myself(self):
    return [ self + i * P(1,0) for i in range(self.length) ]

  def get_neighbors(self):
    myself = self.get_myself()
    return { neighbor for p in myself for neighbor in p.get_neighbors() if not neighbor in myself }
    
class Part(P):
  def __new__(self,x,y,symbol):
    part = super().__new__(Part,x,y)
    part.symbol = symbol
    return part

  def __repr__(self):
    return "Part '{}' at {}".format(self.symbol, super().__repr__())

def read_input():
  parts = {}
  numbers = {}

  for y, line in enumerate(fileinput.input()):
    line = line.strip()
    for part in SYMBOL.finditer(line):
      x = part.start()
      parts[P(x,y)] = Part(x,y,part.group(0))
    for number in NUMBER.finditer(line):
      x = number.start()
      numbers[P(x,y)] = Number(x,y,number.group(0))

  return parts, numbers

    
def main():
  parts, numbers = read_input()
  
  # part 1
  part_numbers = [ number for number in numbers.values() if any(position in parts for position in number.get_neighbors()) ]
  print(sum(number.value for number in part_numbers))

  # part 2
  stars = [ part for part in parts.values() if part.symbol == "*" ]

  stars_with_neighbors = [ (star,[number for number in part_numbers if star in number.get_neighbors()]) for star in stars ]

  gears = [ (star,neighbors) for star,neighbors in stars_with_neighbors if len(neighbors) == 2 ]

  gear_ratios = [ reduce(mul,[n.value for n in neighbors]) for _, neighbors in gears ]

  print(sum(gear_ratios))

if __name__ == "__main__":
  main()
