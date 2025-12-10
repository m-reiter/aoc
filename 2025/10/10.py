#!/usr/bin/python3

import fileinput
from itertools import combinations, combinations_with_replacement

from P import P

ON = "#"
OFF = "."

class Indicators:
  def __init__(self, diagram):
    self.target = tuple( int(char == ON) for char in diagram[1:-1] )

  def __str__(self):
    return f"[{''.join(ON if light else OFF for light in self.target)}]"

  def __repr__(self):
    return f'Indicators("{str(self)}")'

class Button:
  def __init__(self, schematic):
    self.wiring = tuple(map(int, schematic[1:-1].split(",")))

  def __str__(self):
    return f"({','.join(map(str, self.wiring))})"

  def __repr__(self):
    return f'Button("{str(self)}")'

  def max_presses(self, target):
    return min(target[i] for i in self.wiring)

  def effect(self, reference, presses = 1):
    return P(*(presses if joltage in self.wiring else 0 for joltage, _ in enumerate(reference)))

def possible_presses(n_presses, max_presses):
  if len(max_presses) == 1:
    if n_presses <= max_presses[0]:
      yield (n_presses, )
  else:
    for presses in range(min(n_presses, max_presses[0]) + 1):
      for further_presses in possible_presses(n_presses - presses, max_presses[1:]):
        yield (presses, ) + further_presses

class Machine:
  def __init__(self, line):
    diagram, *schematics, joltages = line.strip().split()
    self.indicators = Indicators(diagram)
    self.buttons = [ Button(schematic) for schematic in schematics ]
    self.joltages = tuple(map(int, joltages[1:-1].split(',')))

  def __str__(self):
    return f"{str(self.indicators)} {' '.join(map(str, self.buttons))} {{{','.join(map(str, self.joltages))}}}"

  def __repr__(self):
    return f'Machine("{str(self)}")'

  def solve_part_1(self):
    for i in range(len(self.buttons)):
      for combination in combinations(self.buttons, i + 1):
        outcome = tuple(toggles % 2 for toggles in sum(button.effect(self.indicators.target) for button in combination))
        if outcome == self.indicators.target:
          return i + 1

  def solve_part_2(self):
    max_presses = [ button.max_presses(self.joltages) for button in self.buttons ]
    n_presses = max(self.joltages)
    while True:
      print(self, n_presses)
      for combination in possible_presses(n_presses, max_presses):
        outcome = tuple(sum(button.effect(self.indicators.target, presses) for button, presses in zip(self.buttons, combination)))
        if outcome == self.joltages:
          print("***", n_presses)
          return n_presses
      n_presses = n_presses + 1

def main():
  machines = [ Machine(line) for line in fileinput.input() ]

  # part 1
  print(sum(machine.solve_part_1() for machine in machines))

  # part 2
  print(sum(machine.solve_part_2() for machine in machines))

if __name__ == "__main__":
  main()
