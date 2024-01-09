#!/usr/bin/python3

import fileinput

from P import P

NORTH = P( 0, -1)
SOUTH = P( 0,  1)
EAST  = P( 1,  0)
WEST  = P(-1,  0)

BEAMS = {
  NORTH: "^",
  SOUTH: "v",
  EAST: ">",
  WEST: "<"
}

EMPTY = "."

MIRRORS = {
  "/": {
    NORTH: EAST,
    SOUTH: WEST,
    EAST: NORTH,
    WEST: SOUTH
  },
  "\\": {
    NORTH: WEST,
    SOUTH: EAST,
    EAST: SOUTH,
    WEST: NORTH
  }
}

SPLITTERS = {
  "|": (EAST, WEST),
  "-": (NORTH, SOUTH)
}

def left(p):
  return P(p.y, -p.x)

def right(p):
  return P(-p.y, p.x)

def split(p):
  return left(p), right(p)

class Tile:
  def __init__(self, kind):
    self.kind = kind
    self.clear()

  def clear(self):
    self.energized = False
    self.beams = set()

  def __str__(self):
    if self.kind != EMPTY:
      return self.kind
    if not self.energized:
      return EMPTY
    if len(self.beams) > 1:
      return str(len(self.beams))
    for beam in self.beams:
      return BEAMS[beam]

  def handle(self, beam):
    if beam in self.beams:
      return tuple()
    self.energized = True
    self.beams.add(beam)
    if self.kind in MIRRORS:
      return (MIRRORS[self.kind][beam], )
    elif self.kind in SPLITTERS and beam in SPLITTERS[self.kind]:
      return split(beam)
    else:
      return (beam, )

class Contraption(dict):
  def __init__(self, *args, **kwargs):
    self.dimx = self.dimy = None
    super().__init__(*args, **kwargs)

  def __str__(self):
    return "\n".join(
      "".join(str(self[P(x, y)]) for x in range(self.dimx)) for y in range(self.dimy)
    )

  def energy_map(self):
    return "\n".join(
      "".join("#" if self[P(x, y)].energized else EMPTY for x in range(self.dimx)) for y in range(self.dimy)
    )

  def clear(self):
    for tile in self.values():
      tile.clear()
      
  def populate(self, position = P(0,0), direction = EAST):
    beams = { (position, direction) }

    while beams:
      position, direction = beams.pop()
      
      for new_direction in self[position].handle(direction):
        new_position = position + new_direction
        if new_position in self:
          beams.add((new_position, new_direction))

  def total_energy(self):
    return sum(tile.energized for tile in self.values())

def read_input():
  contraption = Contraption()

  for y, line in enumerate(fileinput.input()):
    for x, char in enumerate(line.strip()):
      contraption[P(x, y)] = Tile(char)

  contraption.dimx = x + 1
  contraption.dimy = y + 1

  return contraption

def part2(contraption):
  starting_states = [ (P(x, 0), SOUTH) for x in range(contraption.dimx) ]
  starting_states += [ (P(x, contraption.dimy - 1), NORTH) for x in range(contraption.dimx) ]
  starting_states += [ (P(0, y), EAST) for y in range(contraption.dimy) ]
  starting_states += [ (P(contraption.dimx - 1, y), WEST) for y in range(contraption.dimy) ]

  results = {}
    
  contraption.clear()

  for state in starting_states:
    contraption.populate(*state)
    results[state] = contraption.total_energy()
    contraption.clear()

  optimum = max(results, key = lambda x: results[x])

  return optimum

  return(contraption)
  
def main():
  contraption = read_input()

  verbose = contraption.dimy < 100

  if verbose:
    print(contraption)
    print()

  # part 1
  contraption.populate()

  if verbose:
    print(contraption)
    print()
    print(contraption.energy_map())
    print()

  print(contraption.total_energy())
  print()

  # part 2
  optimum = part2(contraption)

  contraption.populate(*optimum)

  if verbose:
    print(contraption)
    print()
    print(contraption.energy_map())
    print()

  print(optimum)
  print()

  print(contraption.total_energy())

if __name__ == "__main__":
  main()
