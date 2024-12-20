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
    self.initial = {}
    for line in registers:
      register, value = REGISTER.match(line).groups()
      self.initial[register] = int(value)
    self.program = list(map(int, program[0].split(": ")[1].split(",")))
    self.silent = False
    self.reset()

  def reset(self):
    self.registers = self.initial.copy()
    self.pc = 0
    self.prefix = ''
    self.output = ''

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
    out = f"{self.prefix}{self.combo() % 8}"
    if self.silent:
      self.output += out
    else:
      print(out, end='')
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
        if self.prefix and not self.silent:
          print()
        return

  def correct(self):
    a = 281474976710656
    step = a // 2
    a = 281474975710640
    self.silent = True
    direction = -1
    while True:
      print(a, step)
      a += 1 # direction * step
      self.reset()
      self.registers['A'] = a
      self.run()
      if len(self.output.split(",")) > len(self.program):
        direction = -1
      else:
        direction = 1
      if self.output == ",".join(map(str, self.program)):
        return a
      step = step // 2
      #a -= 1

def read_input():
  registers, programs = split_at(fileinput.input(), is_blank)
  return Computer(registers, programs)
    
def main():
  computer = read_input()

  # part 1
  computer.run(verbose = False)

  # part 2
  print(computer.correct())

if __name__ == "__main__":
  main()
