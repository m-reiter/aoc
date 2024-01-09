#!/usr/bin/python3

import fileinput
from collections import defaultdict

class Computer():
  
  def __init__(self,program):
    self.registers = defaultdict(int)
    self.program = program
    self.pc = 0
    self.sound = None

  def get_value(self,arg):
    try:
      return int(arg)
    except ValueError:
      return self.registers[arg]

  def snd(self,arg):
    self.sound = self.get_value(arg)

  def rcv(self,arg):
    if self.get_value(arg) != 0:
      return True
    else:
      return 1

  def step(self):
    self.last = self.pc
    jump = 1
    instruction, *args = self.program[self.pc]
    if instruction == "snd":
      self.snd(args[0])
    elif instruction == "rcv":
      result = self.rcv(args[0])
      if result is True:
        return True
      else:
        jump = result
    elif instruction == "opt1":
      print(instruction)
      self.registers["a"] *= 2**self.registers["i"]
      jump = int(args[0])
    elif instruction == "opt2":
      print("opt2, i={}".format(self.registers["i"],end="",flush=True))
      p = self.registers["p"]
      a = self.registers["a"]
      for _ in range(self.registers["i"]):
        print(".",end="",flush=True)
        p *= 8505
        p %= a
        p *= 129749
        p += 12345
        p %= a
        self.registers["b"] = p % 10000
        self.snd("b")
      self.registers["p"] = p
      jump = int(args[0])
      print("done")
    elif instruction == "nop":
      print("Caution! nop executed")
    else: # start of 2 argument instructions
      args[1] = self.get_value(args[1])
      if instruction == "set":
        self.registers[args[0]] = args[1]
      elif instruction == "add":
        self.registers[args[0]] += args[1]
      elif instruction == "mul":
        self.registers[args[0]] *= args[1]
      elif instruction == "mod":
        self.registers[args[0]] %= args[1]
      elif instruction == "jgz":
        if self.get_value(args[0]) > 0:
          jump = args[1]
      else:
        raise ValueError
    self.pc += jump
    return jump == 0

  def run(self):
    while True:
      terminated = self.step()
      if terminated:
        return self.sound

class RealComputer(Computer):

  def __init__(self,program,partner=None,ID=0):
    super().__init__(program)
    self.partner = partner
    self.queue = []
    self.ID = self.registers["p"] = ID
    self.snd_count = 0
    self.last = -1

  def accept(self,value):
    self.queue.append(value)

  def snd(self,arg):
    self.partner.accept(self.get_value(arg))
    self.snd_count += 1
#    if self.ID == 1:
#      print("{}: snd {} ({}. send)".format(self.ID,self.get_value(arg),self.snd_count))

  def rcv(self,arg):
    if self.queue:
      self.registers[arg] = self.queue.pop(0)
      return 1
    else:
      return 0

#  def step(self):
#    if self.pc != self.last:
#      print("{}:{:2}: {:10} ({}) {}".format(self.ID,self.pc," ".join(self.program[self.pc]),dict(self.registers),self.queue))
#    return super().step()

def main():

  program = [line.strip().split() for line in fileinput.input()]

  # part 1
  computer = Computer(program)
  print(computer.run())

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
