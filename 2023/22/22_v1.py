#!/usr/bin/python3

import fileinput

from attr import attrs, attrib
from itertools import groupby

from P import P

DOWN = P(0, 0, -1)

@attrs(frozen = True)
class Brick:
  start = attrib()
  direction = attrib()
  length = attrib()

  @classmethod
  def from_line(cls, line):
    points = (P(*(map(int, point.split(",")))) for point in line.split("~"))

    start, end = sorted(points, key = lambda p: p.z)
    
    direction = end - start
    difference = max(direction)
    if difference:
      direction = direction / difference

    return cls(start, direction, difference + 1)

  def __iter__(self):
    return (self.start + i * self.direction for i in range(self.length))

  def __contains__(self, other):
    if isinstance(other, Brick):
      return any(cube in self for cube in other)
    else:
      return other in self.__iter__()

  def __add__(self, other):
    return Brick(self.start + other, self.direction, self.length)

  @property
  def bottom(self):
    return self.start.z

  @property
  def top(self):
    return self.start.z + 1 + (self.length - 1) * self.direction.z

  @property
  def has_landed(self):
    return self.bottom == 1
  
@attrs
class Sand:
  bricks = attrib(factory = list)

  @classmethod
  def from_input(cls):
    return cls(list(Brick.from_line(line) for line in fileinput.input()))

  def can_fall(self, brick):
    if brick.has_landed:
      return False
    for other in self.bricks:
      if brick != other and brick + DOWN in other:
        return False
    return True

  def supports(self, bottom, top):
    return bottom.top == top.bottom and top + DOWN in bottom

  def fall(self, brick):
    self.bricks.remove(brick)

    while self.can_fall(brick):
      brick = brick + DOWN

    self.bricks.append(brick)

  def settle(self):
    bricks = sorted(self.bricks.copy(), key = lambda brick: brick.bottom)

    for i,brick in enumerate(bricks):
      print(i)
      self.fall(brick)

  def old_find_safe_bricks(self):
    safe_bricks = []

    bricks = self.bricks.copy()
    
    for brick in bricks:
      self.bricks.remove(brick)

      if not any(self.can_fall(other) for other in self.bricks):
        safe_bricks.append(brick)

      self.bricks.append(brick)

    return safe_bricks

  def find_safe_bricks(self):
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

def main():
  sand = Sand.from_input()

  # part 1
  sand.settle()
  print(len(sand.find_safe_bricks()))

if __name__ == "__main__":
  main()
