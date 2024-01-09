#!/usr/bin/python3

import fileinput
import re

from functools import reduce
from operator import mul

NUMBER = re.compile("\d+")
SYMBOL = re.compile("[^\d\.]")

class Number():
  def __init__(self,x,y,value):
    self.value = int(value)
    self.x = x
    self.y = y
    self.length = len(value)

  def __repr__(self):
    return "Number {} at {} spanning {} spaces".format(self.value, (self.x,self.y), self.length) 

  def __contains__(self, position):
    return self.x-1 <= position.x <= self.x+self.length and self.y-1 <= position.y <= self.y+1

class Part():
  def __init__(self,x,y,symbol):
    self.x = x
    self.y = y
    self.symbol = symbol

  def __repr__(self):
    return "Part '{}' at {}".format(self.symbol, (self.x,self.y))

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
    
def main():
  parts, numbers = read_input()
  
  # part 1
  part_numbers = [ number for number in numbers if any(part in number for part in parts) ]
  print(sum(number.value for number in part_numbers))

  # part 2
  stars = [ part for part in parts if part.symbol == "*" ]
  stars_with_neighbors = [ (star,[number for number in part_numbers if star in number]) for star in stars ]
  gears = [ (star,neighbors) for star,neighbors in stars_with_neighbors if len(neighbors) == 2 ]
  gear_ratios = [ reduce(mul,[n.value for n in neighbors]) for _, neighbors in gears ]

  print(sum(gear_ratios))

if __name__ == "__main__":
  main()
