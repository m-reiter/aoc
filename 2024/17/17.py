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

class Computer:
  def __init__(self, registers, program):
    self.registers = {}
    for line in registers:
      register, value = REGISTER.match(line).groups()
      self.registers[register] = int(value)
    print(program)
    self.program = list(map(int, program[0].split(": ")[1].split(",")))
    self.pc = 0
    self.prefix = ''

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
    self.registers['B'] = self.registers['B'] | self.literal()
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
    self.registers['B'] = self.registers['B'] | self.registers['C']
    return False

  def out(self):
    print(f"{self.prefix}{self.combo()}")
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

def read_input():
  registers, programs = split_at(fileinput.input(), is_blank)
  return Computer(registers, programs)
    
def main():
  pass

if __name__ == "__main__":
  main()
