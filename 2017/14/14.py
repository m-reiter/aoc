#!/usr/bin/python3

import fileinput
from more_itertools import chunked
from functools import reduce
from operator import xor
from P import P

REGISTERS = 256

ADDITIONAL_LENGTHS = [ 17, 31, 73, 47, 23  ]

INPUT = "jzgqcdpd"
#INPUT = "flqrgnkx"

class Registers(list):
  
  def __init__(self,lengths,iterable=range(REGISTERS)):
    super().__init__(iterable)
    self.position = self.skip = 0
    self.lengths = lengths

  def __getitem__(self,key):
    return super().__getitem__(key % len(self))

  def __setitem__(self,key,value):
    return super().__setitem__(key % len(self),value)

  def step(self,length):
    replace = [ self[self.position+i] for i in range(length) ]
    replace.reverse()
    for i,value in enumerate(replace,self.position):
      self[i] = value
    self.position = (self.position+length+self.skip) % REGISTERS
    self.skip += 1

  def iterate(self):
    for length in self.lengths:
      self.step(length)

def main():

  used = []
  for row in range(128):
    lengths = [ ord(char) for char in "{}-{}".format(INPUT,row) ] + ADDITIONAL_LENGTHS
    registers = Registers(lengths)
    for _ in range(64):
      registers.iterate()
    dense = [ reduce(xor,sparse) for sparse in chunked(registers,16) ]
    for column,value in enumerate("".join("{:08b}".format(i) for i in dense)):
      if value == "1":
        used.append(P(column,row))

  # part 1
  print(len(used))

  # part 2
  regions = 0
  unhandled = set(used)
  while unhandled:
    regions += 1
    to_check = [ unhandled.pop() ]
    while to_check:
      seed = to_check.pop(0)
      for n in seed.get_neighbors(diagonals=False,borders=P(127,127)):
        if n in unhandled:
          unhandled.discard(n)
          to_check.append(n)
  print(regions)

if __name__ == "__main__":
  main()
