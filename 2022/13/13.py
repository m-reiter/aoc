#!/usr/bin/python3

import fileinput
import string
from functools import total_ordering,reduce
from more_itertools import split_at
from operator import mul

ALLOWED_CHARACTERS = set(string.digits+"[],")

def is_blank(line):
  return line.strip() == ""

@total_ordering
class packet(list):

  def __init__(self,iterable):
    super().__init__(iterable)

  def __lt__(self,other):
    if isinstance(other,int):
      other = [other]
    return super().__lt__(other)

  def __gt__(self,other):
    if isinstance(other,int):
      other = [other]
    return super().__gt__(other)

  def __eq__(self,other):
    if isinstance(other,int):
      other = [other]
    return super().__eq__(other)

def read_packets():
  packets = []
  for pair in split_at(fileinput.input(),is_blank):
    pair = tuple((line.strip() for line in pair))
    if not all(set(line) <= ALLOWED_CHARACTERS for line in pair):
      raise ValueError
    pair = tuple(line.replace("[","packet([") for line in pair)
    pair = tuple(line.replace("]","])") for line in pair)
    pair = tuple(eval(line) for line in pair)
    packets.append(pair)
  return packets

def part1(packets):
  return sum(lineno for lineno,(left,right) in enumerate(packets,1) if left < right)

def part2(packets):
  dividers = [packet([packet([2])]),packet([packet([6])])]
  lefts = [left for left,right in packets]
  rights = [right for left,right in packets]
  packets = sorted(lefts+rights+dividers)
  indices = [packets.index(i)+1 for i in dividers]
  return reduce(mul,indices)

def main():
  packets = read_packets()

  print(part1(packets))
  print(part2(packets))

if __name__ == "__main__":
  main()
