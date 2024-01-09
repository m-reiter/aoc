#!/usr/bin/python3

import fileinput
from collections import defaultdict

class Computer():
  
  def __init__(self,program):
    self.registers = { c: 0 for c in "abcdefgh" }
    self.program = program
    self.pc = 0
    self.muls = 0

  def get_value(self,arg):
    try:
      return int(arg)
    except ValueError:
      return self.registers[arg]

  def step(self):
    self.last = self.pc
    jump = 1
    instruction, *args = self.program[self.pc]
    args[1] = self.get_value(args[1])
    if instruction == "set":
      self.registers[args[0]] = args[1]
    elif instruction == "sub":
      self.registers[args[0]] -= args[1]
    elif instruction == "mul":
      self.registers[args[0]] *= args[1]
      self.muls += 1
    elif instruction == "jnz":
      if self.get_value(args[0]) != 0:
        jump = args[1]
    else:
      raise ValueError
    self.pc += jump

  def run(self):
    while self.pc in range(len(self.program)):
      self.step()

class RealComputer(Computer):

#  def __init__(self,program,partner=None,ID=0):
#    super().__init__(program)
#    self.partner = partner
#    self.queue = []
#    self.ID = self.registers["p"] = ID
#    self.snd_count = 0
#    self.last = -1
#
#  def accept(self,value):
#    self.queue.append(value)
#
#  def snd(self,arg):
#    self.partner.accept(self.get_value(arg))
#    self.snd_count += 1
#    if self.ID == 1:
#      print("{}: snd {} ({}. send)".format(self.ID,self.get_value(arg),self.snd_count))

#  def rcv(self,arg):
#    if self.queue:
#      self.registers[arg] = self.queue.pop(0)
#      return 1
#    else:
#      return 0

  def step(self):
    print("{:2}: {:15} ({})".format(self.pc," ".join(self.program[self.pc]),self.registers))
    super().step()

def main():

  program = [line.strip().split() for line in fileinput.input()]

  # part 1
  computer = Computer(program)
  computer.run()
  print(computer.muls)

  # part 2
  computer = RealComputer(program)
  computer.registers["a"] = 1
  computer.run()
  print(computer.registers["h"])
  return

  # part 2
  c0 = RealComputer(program)
  c1 = RealComputer(program,partner=c0,ID=1)
  c0.partner = c1
  
  while True:
    deadlock = c0.step()
    deadlock = c1.step() and deadlock
    if deadlock:
      break

  print(c1.snd_count)

if __name__ == "__main__":
  main()
