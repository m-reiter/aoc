#!/usr/bin/python3

import fileinput

class Console():

  def __init__(self, code):

    self.code = []
    
    for line in code:
      opcode, argument = line.split()
      self.code.append((opcode, int(argument)))

    self.reset()

  def reset(self):

    self.pc = 0
    self.accumulator = 0
    
  def acc(self, argument):

    self.accumulator += argument
    self.pc += 1

  def jmp(self, argument):

    self.pc += argument

  def nop(self, argument):

    self.pc += 1

  def step(self):

    opcode, argument = self.code[self.pc]
    self.__getattribute__(opcode)(argument)

  def find_loop(self):

    self.reset()

    visited = set()

    while self.pc not in visited:
      visited.add(self.pc)
      self.step()
      if self.pc == len(self.code):
        return False

    return self.accumulator

  def fix(self):

    replacements = { "jmp": "nop", "nop": "jmp" }

    for lineno, (opcode,argument) in enumerate(self.code):
      if opcode in replacements:
        self.code[lineno] = (replacements[opcode],argument)
        if not self.find_loop():
          return True
        self.code[lineno] = (opcode,argument)

    return False
      

def main():
  
  console = Console([line.strip() for line in fileinput.input()])
  
  print(console.find_loop())

  console.fix()
  print(console.accumulator)

if __name__ == "__main__":
  main()
