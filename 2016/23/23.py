#!/usr/bin/python3

import fileinput
from collections import UserDict

EGGS = 12

class Computer(UserDict):
  def __init__(self,program,init={}):
    super().__init__()
    self.program = program
    self.pc = 0
    for register in "abcd":
      self[register] = 0
    self.update(init)
    self.overrides = []

  def __repr__(self):
    return "Computer, pc = {}, a: {}, b: {}, c: {}, d: {}".format(self.pc,*(self[x] for x in "abcd"))

  def step(self,verbose=True):
    if verbose:
      print("a: {:3d} b: {:3d} c: {:3d} d: {:3d}. Executing step {:2d}: {}".format(*(self[x] for x in "abcd"),self.pc," ".join(self.program[self.pc])))
    for r in self.overrides:
      if self.pc in r:
        exec(self.overrides[r])
        self.pc = r.stop
        return
    instruction, *args = self.program[self.pc]
    if instruction == "cpy":
      x,y = args
      try:
        value = int(x) 
      except ValueError:
        value = self[x]
      self[y] = value
    elif instruction == "inc":
      self[args[0]] += 1
    elif instruction == "dec":
      self[args[0]] -= 1
    elif instruction == "jnz":
      x,y = args
      try:
        value = int(x) 
      except ValueError:
        value = self[x]
      if value != 0:
        try:
          y = int(y) 
        except ValueError:
          y = self[y]
        self.pc += int(y)-1
    elif instruction == "tgl":
      x = args[0]
      try:
        x = int(x) 
      except ValueError:
        x = self[x]
      target = self.pc+x
      if any(target in r for r in self.overrides):
        print("*** Oopsie! toggling pc={} ***".format(target))
      if target in range(len(self.program)):
        if self.program[target][0] == "inc":
          self.program[target][0] = "dec"
        elif self.program[target][0] == "jnz":
          self.program[target][0] = "cpy"
        elif len(self.program[target]) == 2:
          self.program[target][0] = "inc"
        else:
          self.program[target][0] = "jnz"
    else:
      raise ValueError
    self.pc += 1
    if verbose:
      pass
      #print("new state: {}".format(self))

  def run(self):
    while self.pc < len(self.program):
      self.step()

def main():
  program = [line.strip().split() for line in fileinput.input()]
  computer = Computer(program,init = {"a": EGGS})
  computer.overrides = {
    range(2,10): "self['a'] = self['a']*self['b']; self['c']=self['d']=0",
    range(21,26): "self['a'] += self['c']*self['d']; self['c']=self['d']=0"
  }
  print(computer)
  computer.run()
  print(computer)

if __name__ == "__main__":
  main()
