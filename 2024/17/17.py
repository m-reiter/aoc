#!/usr/bin/python3

import fileinput
import re
from more_itertools import split_at

REGISTER = re.compile("Register (.): (\d+)")

COMBO_TO_REGISTER = {
  4: 'A',
  5: 'B',
  6: 'C'
}

def is_blank(line):
  return not(line.strip())

def red(s):
  return "\033[31m"+str(s)+"\033[0m"

class Computer:
  def __init__(self, registers, program):
    self.registers = {}
    for line in registers:
      register, value = REGISTER.match(line).groups()
      self.registers[register] = int(value)
    self.program = list(map(int, program[0].split(": ")[1].split(",")))
    self.pc = 0
    self.prefix = ''

  def __str__(self):
    s = "\n".join(f"Register {k}: {v}" for k,v in self.registers.items())
    s += "\n\nProgram: "
    s += ",".join(f"{byte}" if self.pc != i else red(byte) for i,byte in enumerate(self.program))
    return s

  def literal(self):
    return self.program[self.pc + 1]

  def combo(self):
    combo = self.literal()
    if combo <= 3:
      return combo
    if combo == 7:
      raise ValueError
    return self.registers[COMBO_TO_REGISTER[combo]]

  def xdv(self, register):
    self.registers[register] = self.registers['A'] // (2 ** self.combo())
    return False

  adv = lambda self: Computer.xdv(self, 'A')
  bdv = lambda self: Computer.xdv(self, 'B')
  cdv = lambda self: Computer.xdv(self, 'C')

  def bxl(self):
    self.registers['B'] = self.registers['B'] ^ self.literal()
    return False

  def bst(self):
    self.registers['B'] = self.combo() % 8
    return False

  def jnz(self):
    if self.registers['A'] == 0:
      return False
    self.pc = self.literal()
    return True

  def bxc(self):
    self.registers['B'] = self.registers['B'] ^ self.registers['C']
    return False

  def out(self):
    print(f"{self.prefix}{self.combo() % 8}", end='')
    self.prefix = ','
    return False

  OPCODE_TO_INSTRUCTION = {
    0: adv,
    1: bxl,
    2: bst,
    3: jnz,
    4: bxc,
    5: out,
    6: bdv,
    7: cdv
  }

  def step(self):
    if not Computer.OPCODE_TO_INSTRUCTION[self.program[self.pc]](self):
      self.pc += 2

  def run(self, verbose = False):
    if verbose:
      print(f"{self}\n")
    while True:
      try:
        self.step()
        if verbose:
          print(f"{self}\n")
      except IndexError:
        if self.prefix:
          print()
        return

def read_input():
  registers, programs = split_at(fileinput.input(), is_blank)
  return Computer(registers, programs)
    
def main():
  computer = read_input()

  # part 1
  computer.run(verbose = False)

if __name__ == "__main__":
  main()
