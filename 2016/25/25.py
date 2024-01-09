#!/usr/bin/python3

import fileinput
from collections import UserDict

class Computer(UserDict):
  def __init__(self,program,a=None):
    super().__init__()
    self.program = program
    self.pc = 0
    self.last_output = 1
    for register in "abcd":
      self[register] = 0
    if a:
      self["a"] = a

  def __repr__(self):
    return "Computer, pc = {}, a: {}, b: {}, c: {}, d: {}".format(self.pc,*(self[x] for x in "abcd"))

  def tuple(self):
    return tuple(self[x] for x in "abcd") + (self.pc,self.last_output)

  def step(self,verbose=False):
    if verbose:
      print("executing step {}: {}".format(self.pc,self.program[self.pc]))
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
      if target in range(len(self.program)):
        if self.program[target][0] == "inc":
          self.program[target][0] = "dec"
        elif self.program[target][0] == "jnz":
          self.program[target][0] = "cpy"
        elif len(self.program[target]) == 2:
          self.program[target][0] = "inc"
        else:
          self.program[target][0] = "jnz"
    elif instruction == "out":
      x = args[0]
      try:
        x = int(x) 
      except ValueError:
        x = self[x]
      if x != 1-self.last_output:
        raise ValueError
      else:
        self.last_output = x
        print(x)
    else:
      raise ValueError
    self.pc += 1
    if verbose:
      print("new state: {}".format(self))

  def run(self):
    while self.pc < len(self.program):
      self.step()

  def run_till_repeat(self):
    past_states = { self.tuple() }
    while self.pc < len(self.program):
      try:
        self.step()
      except ValueError:
        return False
      if self.tuple() in past_states:
        return True
      past_states.add(self.tuple())

def main():
  program = [line.strip().split() for line in fileinput.input()]
  a = 0
  while True:
    computer = Computer(program,a=a)
    print(computer)
    if computer.run_till_repeat():
      break
    a += 1
  print(a)
  print(computer)

if __name__ == "__main__":
  main()
