from itertools import product
from math import sqrt

class P(tuple):

  @staticmethod
  def offsets(dimensions = 2, diagonals=True):
    #return [P(x,y) for x in range(-1,2) for y in range(-1,2) if (x or y) and (diagonals or not x*y)]
    return [ P(*coords) for coords in product(range(-1,2), repeat = dimensions)
             if any(coords) # exclude 0-vector
             and (diagonals or sum(map(abs,coords)) == 1) ]

  def __new__(cls,*args):
    return super().__new__(cls,args)

  def __repr__(self):
    return "P{}".format(super().__repr__())

  def __abs__(self):
    return sqrt(sum(x**2 for x in self))

  def __neg__(self):
    return self * -1

  def __add__(self, other):

    return P(*(s + o for s,o in zip(self, other)))

  def __sub__(self, other):

    return P(*(s - o for s,o in zip(self, other)))

  def __mul__(self, integer):

    return P(*(s * integer for s in self))

  __rmul__ = __mul__

  @property
  def x(self):

    return self[0]

  @property
  def y(self):

    return self[1]

  @property
  def z(self):

    return self[2]

  def get_neighbors(self,diagonals=True,borders=False,cyclic=False):
    neighbors = [self + offset for offset in P.offsets(dimensions = len(self), diagonals = diagonals)]
    if borders:
      if cyclic:
        neighbors = [ P(*(x % b for x,b in zip(n, borders))) for n in neighbors ]
      else:
        neighbors = [ n for n in neighbors if all(0 <= x <= b for x,b in zip(n, borders)) ]
    return neighbors
