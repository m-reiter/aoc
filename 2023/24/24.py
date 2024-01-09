#!/usr/bin/python3

import fileinput
import sympy as sym

from attr import attrs, attrib
from itertools import combinations

from P import P

AREAMIN = 200000000000000
AREAMAX = 400000000000000

@attrs
class Hailstone:
  start = attrib()
  velocity = attrib()

  @classmethod
  def from_line(cls, line):
    points = line.split(" @ ")
    start, velocity = (P(*map(int, point.split(", "))) for point in points)
    return cls(start, velocity)

  def __attrs_post_init__(self):
    """ calculate parameters for 2D line equation y = m x + b and some other helpers
    """
    try:
      self.m = self.velocity.y / self.velocity.x
      self.b = self.start.y - self.start.x * self.m
      self.is_vertical = False
    except ZeroDivisionError:
      self.is_vertical = True
      raise ZeroDivisionError

  def position(self, t):
    """ return own position at time t
    """
    return self.start + t * self.velocity

  def t(self, x):
    """ return time at which self.x == x
    """
    return (x - self.start.x) / self.velocity.x

  def collides_in_xy(self, other):
    """ returns
        - False if both trajectories don't cross
        - True if both trajectories are identical
        - (x, y, t1, t2) = x and y coordinate of intersection and times when self and other are there
    """
    if self.m == other.m:
      return self.b == other.b
    else:
      x = (self.b - other.b) / (other.m - self.m)
      y = self.m * x + self.b
      t1 = self.t(x)
      t2 = other.t(x)

      return x, y, t1, t2

  def will_collide_in_area(self, other):
    collision = self.collides_in_xy(other)

    if isinstance(collision, bool):
      return collision
    else:
      x, y, t1, t2 = collision

      return AREAMIN <= x <= AREAMAX and AREAMIN <= y <= AREAMAX and t1 >= 0 and t2 >= 0 

def find_something(first, second, third):
  """ sx + t1 * vx = s1 + t1 * v1
      sx = s1 + (v1 - vx) * t1

      sx + t2 * vx = s2 + t2 * v2
      s1 + (v1 - vx) * t1 + t2 * vx = s2 +t2 * v2
      vx * (t2 - t1) = s2 - s1 + t2 * v2 - t1 * v1
      vx = (s2 - s1 + t2 * v2 - t1 * v1) / (t2 - t1)
      
      sx + t3 * vx = s3 + t3 * v3
      s1 + (v1 - (s2 - s1 + t2 * v2 - t1 * v1) / (t2 - t1)) * t1 + t3 * (s2 - s1 + t2 * v2 - t1 * v1) / (t2 - t1) = s3 + t3 * v3

      x1 + (vx1 - (x2 - x1 + t2 * vx2 - t1 * vx1) / (t2 - t1)) * t1 + t3 * (x2 - x1 + t2 *vx2 - t1 * vx1) / (t2 - t1) = x3 + t3 * vx3
      y1 + (vy1 - (y2 - y1 + t2 * vy2 - t1 * vy1) / (t2 - t1)) * t1 + t3 * (y2 - y1 + t2 *vy2 - t1 * vy1) / (t2 - t1) = y3 + t3 * vy3
      z1 + (vz1 - (z2 - z1 + t2 * vz2 - t1 * vz1) / (t2 - t1)) * t1 + t3 * (z2 - z1 + t2 *vz2 - t1 * vz1) / (t2 - t1) = z3 + t3 * vz3

      t3 = (x3 + x1 + (vx1 - (x2 - x1 + t2 * vx2 - t1 * vx1) / (t2 - t1)) * t1) / ((x2 - x1 + t2 *vx2 - t1 * vx1) / (t2 - t1) - vx3)

      X + t3 * VX = x3 + t3 * vx3
      Y + t3 * VY = y3 + t3 * vy3
      Z + t3 * VZ = z3 + t3 * vz3
  """
  x1, y1, z1 = first.start
  vx1, vy1, vz1 = first.velocity
  x2, y2, z2 = second.start
  vx2, vy2, vz2 = second.velocity
  x3, y3, z3 = third.start
  vx3, vy3, vz3 = third.velocity

  t1, t2, t3 = sym.symbols("t1 t2 t3")

  t1 = sym.solve(x1 + (vx1 - (x2 - x1 + t2 * vx2 - t1 * vx1) / (t2 - t1)) * t1 + t3 * (x2 - x1 + t2 *vx2 - t1 * vx1) / (t2 - t1) - x3 - t3 * vx3, t1)
  assert len(t1) == 1
  t1 = t1[0]
  print(t1)

  t2 = sym.solve(y1 + (vy1 - (y2 - y1 + t2 * vy2 - t1 * vy1) / (t2 - t1)) * t1 + t3 * (y2 - y1 + t2 *vy2 - t1 * vy1) / (t2 - t1) - y3 - t3 * vy3, t2)
  assert len(t2) == 1
  t2 = t2[0]
  print(t2)

  t3 = sym.solve(z1 + (vz1 - (z2 - z1 + t2 * vz2 - t1 * vz1) / (t2 - t1)) * t1 + t3 * (z2 - z1 + t2 *vz2 - t1 * vz1) / (t2 - t1) - z3 - t3 * vz3, t3)
  assert len(t3) == 1
  t3 = t3[0]
  print(t3)

  p3 = first.position(t3)
  print(p3)
  p2 = second.position(t2)
  print(p2)
  direction = p3 - p2
  print(direction)
  velocity = direction * 1.0 / (t3 - t2)
  print(velocity)
  origin = Hailstone(p2, velocity).position(-t2)
  print(origin)

  return Hailstone(origin, velocity)

def main():
  return
  hailstones = list(Hailstone.from_line(line) for line in fileinput.input())

  if len(hailstones) < 10:
    global AREAMIN, AREAMAX
    AREAMIN = 7
    AREAMAX = 27

  # part 1
  print(sum(hailstone.will_collide_in_area(other) for hailstone, other in combinations(hailstones, 2)))

  # part 2
  candidate = find_something(*hailstones[:3])
  print(candidate)

  print(sum(candidate.start))

if __name__ == "__main__":
  main()
