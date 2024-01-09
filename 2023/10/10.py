#!/usr/bin/python3

import fileinput

from collections import defaultdict
from termcolor import colored

from P import P

PIPES = defaultdict(set, {
  '|': { P(0,-1), P(0,1) },
  '-': { P(1,0),  P(-1,0) },
  'L': { P(0,-1), P(1,0) },
  'J': { P(0,-1), P(-1,0) },
  '7': { P(-1,0), P(0,1) },
  'F': { P(1,0),  P(0,1) }
})
GROUND = '.'
START = 'S'

DRAWCHARS = {
  '|': '\u2503',
  '-': '\u2501',
  'L': '\u2517',
  'J': '\u251b',
  '7': '\u2513',
  'F': '\u250f',
  GROUND: '*',
  START: START
}

NEIGHBOURS = {
  'left': {
    ("-",P(1,0)):   (P(0,-1), ),
    ("J",P(1,0)):   tuple(),
    ("7",P(1,0)):   (P(0,-1), P(1,-1), P(1,0)),
    ("-",P(-1,0)):  (P(0,1), ),
    ("F",P(-1,0)):  tuple(),
    ("L",P(-1,0)):  (P(0,1), P(-1,1), P(-1,0)),
    ("|",P(0,-1)):  (P(-1,0), ),
    ("7",P(0,-1)):  tuple(),
    ("F",P(0,-1)):  (P(-1,0), P(-1,-1), P(0,-1)),
    ("|",P(0,1)):   (P(1,0), ),
    ("L",P(0,1)):   tuple(),
    ("J",P(0,1)):   (P(1,0), P(1,1), P(0,1))
  },
  'right': {
    ("-",P(1,0)):   (P(0,1), ),
    ("7",P(1,0)):   tuple(),
    ("J",P(1,0)):   (P(0,1), P(1,1), P(1,0)),
    ("-",P(-1,0)):  (P(0,-1), ),
    ("L",P(-1,0)):  tuple(),
    ("F",P(-1,0)):  (P(0,-1), P(-1,-1), P(-1,0)),
    ("|",P(0,-1)):  (P(1,0), ),
    ("F",P(0,-1)):  tuple(),
    ("7",P(0,-1)):  (P(1,0), P(1,-1), P(0,-1)),
    ("|",P(0,1)):   (P(-1,0), ),
    ("J",P(0,1)):   tuple(),
    ("L",P(0,1)):   (P(-1,0), P(-1,1), P(0,1))
  }
}

class Tile():
  def __init__(self, kind, position):
    self.position = position
    self.kind = kind
    self.is_pipe = kind in PIPES
    self.connections = { position + vector for vector in PIPES[kind] }
    self._to = None
    self.in_loop = False
    self.is_outer = False

  def __repr__(self):
    return '{}("{}", {})'.format(self.__class__.__name__, self.kind, self.position)

  def can_connect_from(self, other):
    return self.is_pipe and other.position in self.connections

  def connect_to(self, other):
    self._to = other

  def find_next_position(self, source):
    candidates = self.connections - { source.position }
    if len(candidates) != 1:
      raise ValueError
    return candidates.pop()

class Maze(dict):
  def __init__(self):
    self.start = None
    self.dimensions = None
    self.loop = None
    self.fancy_printing = False

  def __repr__(self):
    rpr = "<Maze"
    if self.dimensions:
      rpr += " ({}x{})".format(self.dimensions.x, self.dimensions.y)
    if self.start:
      rpr += ", start at ({},{})".format(self.start.x, self.start.y)
    if self.loop:
      rpr +=", loop length {}".format(self.loop)
    return "{} at {}>".format(rpr, hex(id(self)))

  def __str__(self):
    lines = []
    for y in range(self.dimensions.y):
      line = []
      for x in range(self.dimensions.x):
        pos = P(x,y)
        tile = self[pos]
        if self.fancy_printing:
          char = DRAWCHARS[tile.kind]
          if not tile.in_loop:
            char = DRAWCHARS[GROUND]
          if pos == self.start:
            char = colored(char, "blue")
          elif tile.in_loop:
            char = colored(char, "red")
          elif tile.is_outer:
            char = colored(char, "green")
        else:
          char = tile.kind
        line.append(char)
      lines.append("".join(line))
    return "\n".join(lines)

  def check_loop(self, candidate):
    origin = self[self.start]

    loop = [ candidate ]

    while True:
      if not candidate.can_connect_from(origin):
        return 0, None
      if origin.is_pipe:
        origin.connect_to(candidate)
      nxt = candidate.find_next_position(origin)
      if nxt == self.start:
        for pipe in loop:
          pipe.in_loop = True
        return len(loop), candidate
      origin = candidate
      candidate = self[nxt]
      loop.append(candidate)

  def find_loop(self):
    candidates = [ self[pos] for pos in self.start.get_neighbors(diagonals = False, borders = self.dimensions - P(1,1)) ]
    for candidate in candidates:
      length, endpoint = self.check_loop(candidate)
      if length:
        break
    start_connections = { candidate.position - self.start, endpoint.position - self.start }
    for kind, connections in PIPES.items():
      if connections == start_connections:
        start_pipe = Tile(kind, self.start)
        start_pipe.in_loop = True
        start_pipe.connect_to(candidate)
        endpoint.connect_to(start_pipe)
        self[self.start] = start_pipe
        break
    self.loop = length
    
  def find_outer(self, seeds = None):
    if seeds:
      to_check = list(seeds)
    else:
      to_check = [ P(x, 0) for x in range(self.dimensions.x) ]
      to_check.extend([ P(x, self.dimensions.y - 1) for x in range(self.dimensions.x) ])
      to_check.extend([ P(0, y) for y in range(1, self.dimensions.y - 1) ])
      to_check.extend([ P(self.dimensions.x - 1, y) for y in range(1, self.dimensions.y - 1) ])
    
    checked = set()

    while to_check:
      current = to_check.pop(0)
      if current in checked or self[current].in_loop:
        continue
      self[current].is_outer = True
      checked.add(current)
      to_check.extend(n for n in current.get_neighbors(diagonals = False, borders = self.dimensions - P(1,1)) if not n in checked)

  def find_outside_direction(self):
    current = self[self.start]

    while True:
      step = current._to.position - current.position
      current = current._to
      for direction, offsets in NEIGHBOURS.items():
        try:
          if any(self[current.position + offset].is_outer for offset in offsets[(current.kind, step)]):
            return direction
        except KeyError:
          pass

  def find_exclaves(self):
    direction = self.find_outside_direction()

    seeds = set()

    current = self[self.start]

    while True:
      step = current._to.position - current.position
      current = current._to
      for offset in NEIGHBOURS[direction][(current.kind, step)]:
        position = current.position + offset
        if position in self and not self[position].is_outer and not self[position].in_loop:
          seeds.add(position)
      if current.position == self.start:
        break

    self.find_outer(seeds)

def read_input():
  maze = Maze()
  for y, line in enumerate(fileinput.input()):
    for x, char in enumerate(line.strip()):
      maze[P(x,y)] = Tile(char, P(x,y))
      if char == START:
        maze.start = P(x,y)

  maze.dimensions = P(x + 1, y + 1)

  return maze

def main():
  maze = read_input()

  print(maze)
  print()

  maze.find_loop()
  maze.fancy_printing = True

  print(maze)
  print()

  # part 1
  print((maze.loop + 1) // 2)

  # part 2
  maze.find_outer()
  
  print(maze)
  print()

  maze.find_exclaves()
  
  print(maze)
  print()

  print(len([m for m in maze.values() if not m.is_outer and not m.in_loop]))

if __name__ == "__main__":
  pass
  main()
