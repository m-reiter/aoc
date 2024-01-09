#!/usr/bin/python3

import fileinput

from attr import attrs, attrib
from itertools import groupby, combinations
from collections import defaultdict

from P import P

DOWN = P(0, 0, -1)

@attrs()
class Brick:
  max_id = 0

  id = attrib()
  points = attrib()

  def __attrs_post_init__(self):
    self.bottom = min(p.z for p in self.points)
    self.top = max(p.z for p in self.points) + 1

  @classmethod
  def from_line(cls, line):
    points = (P(*(map(int, point.split(",")))) for point in line.split("~"))

    start, end = sorted(points, key = lambda p: p.z)
    
    direction = end - start
    difference = max(direction)
    if difference:
      direction = direction / difference

    cls.max_id += 1

    return cls(cls.max_id, [ start + i * direction for i in range(difference + 1) ])

  def __iter__(self):
    return self.points

  def __contains__(self, other):
    if isinstance(other, Brick):
      return any(cube in self for cube in other.points)
    else:
      return other in self.points

  def __add__(self, other):
    return Brick(self.id, [ p + other for p in self.points ])

  @property
  def has_landed(self):
    return self.bottom == 1

  def supports(self, other):
    return self.top == other.bottom and other + DOWN in self
  
@attrs
class Sand:
  bricks = attrib(factory = list)
  supports = attrib(factory = lambda: defaultdict(set))
  essentials = attrib(factory = set)

  @classmethod
  def from_input(cls):
    return cls(list(Brick.from_line(line) for line in fileinput.input()))

  def can_fall(self, brick):
    if brick.has_landed:
      return False
    for other in self.bricks:
      if brick != other and other.supports(brick):
        return False
    return True

  def fall(self, brick):
    self.bricks.remove(brick)

    while self.can_fall(brick):
      brick = brick + DOWN

    self.bricks.append(brick)

  def settle(self):
    bricks = sorted(self.bricks.copy(), key = lambda brick: brick.bottom)

    for i,brick in enumerate(bricks):
      self.fall(brick)

  def tmp_find_safe_bricks(self):
    safe_bricks = []

    bricks = self.bricks.copy()
    
    for brick in bricks:
      self.bricks.remove(brick)

      if not any(self.can_fall(other) for other in self.bricks):
        safe_bricks.append(brick)

      self.bricks.append(brick)

    return safe_bricks

  def new_find_safe_bricks(self):
    layers = dict(groupby(self.bricks, lambda b: b.bottom))
#    layers = { brick.bottom for brick in self.bricks }
#    layers = { height: [ brick for brick in self.bricks  if brick.bottom == height ] for height in layers }

    print(layers)

    supports = [ { bottom for bottom in self.bricks if self.supports(bottom, top) } for top in self.bricks ]
    
    unsafe_bricks = (support for support in supports if len(support) == 1)

    safe_bricks = set(self.bricks)

    for unsafe in unsafe_bricks:
      safe_bricks = safe_bricks - unsafe

    return safe_bricks

  def find_supports(self):
    for brick, other in combinations(self.bricks, 2):
      if brick.supports(other):
        self.supports[other.id].add(brick.id)

  def find_essentials(self):
    self.essentials = { brick for ontop, below in self.supports.items() if len(below) == 1 for brick in below }

  def count_falling(self):
    self.bricks.sort(key = lambda b: b.top)

    falling = 0

    for i, brick in enumerate(self.bricks):
      removed = { brick.id }
      
      for other in self.bricks[i + 1:]:
        if not other.has_landed and self.supports[other.id].issubset(removed):
          removed.add(other.id)

      falling += len(removed) - 1

    return(falling)

def main():
  sand = Sand.from_input()

  # part 1
  sand.settle()
  sand.find_supports()
  sand.find_essentials()

  print(len(sand.bricks) - len(sand.essentials))

  #part 2
  print(sand.count_falling())

if __name__ == "__main__":
  main()
