#!/usr/bin/python3

import fileinput
from more_itertools import chunked
from functools import reduce
from operator import xor

REGISTERS = 256
#REGISTERS = 5

ADDITIONAL_LENGTHS = [ 17, 31, 73, 47, 23  ]

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
  inputs = [ line.strip() for line in fileinput.input() ]

  # part 1
  lengths = [ int(x) for x in inputs[0].split(",") ]
  registers = Registers(lengths)
  registers.iterate()
  print(registers[0]*registers[1])

  # part 2
  for line in inputs:
    lengths = [ ord(char) for char in line ] + ADDITIONAL_LENGTHS
    registers = Registers(lengths)
    for _ in range(64):
      registers.iterate()
    dense = [ reduce(xor,sparse) for sparse in chunked(registers,16) ]
    print("".join("{:02x}".format(i) for i in dense))

if __name__ == "__main__":
  main()
