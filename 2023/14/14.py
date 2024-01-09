#!/usr/bin/python3

import fileinput

from P import P

ROUNDED = "O"
CUBE = "#"
WALL = "*"
EMPTY = "."

# direction vector and sorting function
TILT = {
  'north':   (P( 0, -1), lambda p: p.y),
  'south':   (P( 0,  1), lambda p: -p.y),
  'west':   (P(-1,  0), lambda p: p.x),
  'east':   (P( 1,  0), lambda p: -p.x)
}

CYCLES = 1000000000

class Platform:
  def __init__(self):
    self.rocks = {
      ROUNDED: [],
      CUBE: []
    }
    self.dimx = self.dimy = None

  @classmethod
  def from_input(cls):
    platform = cls()

    for y, line in enumerate(fileinput.input()):
      for x, char in enumerate(line.strip()):
        if char != EMPTY:
          platform.add_rock(char, x, y)

    platform.dimx = x + 1
    platform.dimy = y + 1

    return platform

  def __getitem__(self, key):
    for kind, positions in self.rocks.items():
      if key in positions:
        return kind

    if 0 <= key.x < self.dimx and 0 <= key.y < self.dimy:
      return EMPTY

    return WALL

  def __str__(self):
    return "\n".join(
      "".join(self[P(x,y)] for x in range(self.dimx))
      for y in range(self.dimy)
    )

  def add_rock(self, rock, x, y):
    self.rocks[rock].append(P(x, y))

  def tilt(self, direction):
    rolling = self.rocks[ROUNDED]
    self.rocks[ROUNDED] = []
    
    step, sorting = TILT[direction]

    for rock in sorted(rolling, key = sorting):
      while self[rock + step] == EMPTY:
        rock = rock + step
      self.rocks[ROUNDED].append(rock)

  def cycle(self):
    for direction in ("north", "west", "south", "east"):
      self.tilt(direction)

  @property
  def load(self):
    return sum(self.dimy - rock.y for rock in self.rocks[ROUNDED])

def main():
  platform = Platform.from_input()

  # part 1
  platform.tilt("north")
  print(platform.load)

  # part 2
  states = [ set(platform.rocks[ROUNDED]) ]
  for i in range(CYCLES):
    platform.cycle()
    state = set(platform.rocks[ROUNDED])
    if state in states:
      break
    states.append(state)

  print(i, states.index(state), len(states))

  for _ in range((CYCLES - i - 1) % (len(states) - states.index(state))):
    platform.cycle()

  print(platform.load)

if __name__ == "__main__":
  main()
