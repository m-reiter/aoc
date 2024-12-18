#!/usr/bin/python3

import fileinput
import re
from more_itertools import split_at

CLAWMACHINE = re.compile("""\
Button A: X\+(\d+), Y\+(\d+)
Button B: X\+(\d+), Y\+(\d+)
Prize: X=(\d+), Y=(\d+)""")

def is_blank(line):
  return not(line.strip())

class ClawMachine:
  def __init__(self, description):
    Ax, Ay, Bx, By, Px, Py = map(int, CLAWMACHINE.match(description).groups())
    self.Ax = Ax
    self.Ay = Ay
    self.Bx = Bx
    self.By = By
    self.Px = Px
    self.Py = Py
    self.a = self.b = 0

  def __repr__(self):
    return f"<Clawmachine, A=({self.Ax}, {self.Ay}), B=({self.Bx}, {self.By}), P=({self.Px}, {self.Py})>"

  def win(self):
    if self.Ax / self.Ay == self.Bx / self.By:
      raise NotImplementedError
    a = (self.Py - self.By * self.Px / self.Bx) / (self.Ay - (self.By * self.Ax / self.Bx))
    a = round(a)
    b = round((self.Px - self.Ax * a) / self.Bx)
    if a * self.Ax + b * self.Bx == self.Px and a * self.Ay + b * self.By == self.Py:
        self.a = a
        self.b = b
    return self.cost()

  def cost(self):
    return 3 * self.a + self.b

def main():
  machines = [ ClawMachine("".join(description)) for description in split_at(fileinput.input(), is_blank) ]

  # part 1
  print(sum(map(ClawMachine.win, machines)))

  # part 2
  for machine in machines:
    machine.Px = 10000000000000 + machine.Px
    machine.Py = 10000000000000 + machine.Py
    machine.a = machine.b = 0
  print(sum(map(ClawMachine.win, machines)))

if __name__ == "__main__":
  main()
