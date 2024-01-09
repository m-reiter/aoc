#!/usr/bin/python3

import fileinput

from P import P

class Cavern(dict):
  @classmethod
  def from_input(cls):
    cavern = cls()

    for y, line in enumerate(fileinput.input()):
      for x, octopus in enumerate(line.strip()):
        cavern[P(x,y)] = int(octopus)

    cavern.borders = P(x,y)

    cavern.steps = 0

    return cavern

  @property
  def size(self):
    return (self.borders.x + 1) * (self.borders.y + 1)

  def step(self):
    self.steps += 1

    for octopus in self:
      self[octopus] += 1

    return self.flash()

  def flash(self):
    flashed = []
    while True:
      flashers = [ octopus for octopus, energy in self.items() if energy > 9 and not octopus in flashed ]
      
      if not flashers:
        break
      
      for flasher in flashers:
        for neighbor in flasher.get_neighbors(borders = self.borders):
          self[neighbor] += 1

      flashed.extend(flashers)

    for octopus in flashed:
      self[octopus] = 0

    return len(flashed)

def main():
  cavern = Cavern.from_input()

  # part 1
  print(sum(cavern.step() for _ in range(100)))

  # part 2
  while True:
    if cavern.step() == cavern.size:
      break

  print(cavern.steps)

if __name__ == "__main__":
  main()
