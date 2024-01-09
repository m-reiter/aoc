#!/usr/bin/python3

import fileinput
from collections import UserDict

class Computer(UserDict):
  def __init__(self,program,c=None):
    super().__init__()
    self.program = program
    self.pc = 0
    for register in "abcd":
      self[register] = 0
    if c:
      self["c"] = 1

  def __repr__(self):
    return "Computer, pc = {}, a: {}, b: {}, c: {}, d: {}".format(self.pc,*(self[x] for x in "abcd"))

  def step(self,verbose=False):
    if verbose:
      print("executing step {}: {}".format(self.pc,self.program[self.pc]))
    instruction, *args = self.program[self.pc].split()
    if instruction == "cpy":
      x,y = args
      value = int(x) if x.isnumeric() else self[x]
      self[y] = value
    elif instruction == "inc":
      self[args[0]] += 1
    elif instruction == "dec":
      self[args[0]] -= 1
    elif instruction == "jnz":
      x,y = args
      value = int(x) if x.isnumeric() else self[x]
      if value != 0:
        self.pc += int(y)-1
    else:
      raise ValueError
    self.pc += 1
    if verbose:
      print("new state: {}".format(self))

  def run(self):
    while self.pc < len(self.program):
      self.step()

def main():
  program = [line.strip() for line in fileinput.input()]
  computer = Computer(program)
  print(computer)
  computer.run()
  print(computer)
  computer = Computer(program,c=1)
  print(computer)
  computer.run()
  print(computer)

if __name__ == "__main__":
  main()
