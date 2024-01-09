class P(tuple):

  @staticmethod
  def offsets(diagonals=True):
    return [P(x,y) for x in range(-1,2) for y in range(-1,2) if (x or y) and (diagonals or not x*y)]

  def __new__(subclass,x,y):
    return tuple.__new__(subclass,(x,y))

  def __add__(self, other):

    return P(self.x+other.x,self.y+other.y)

  def __mul__(self, integer):

    return P(self.x*integer,self.y*integer)

  __rmul__ = __mul__

  @property
  def x(self):

    return self[0]

  @property
  def y(self):

    return self[1]

  def get_neighbors(self,diagonals=True,borders=False,cyclic=False):
    neighbors = [self + offset for offset in P.offsets(diagonals=diagonals)]
    if borders:
      if cyclic:
        neighbors = [P(x % borders.x,y % borders.y) for x,y in neighbors]
      else:
        neighbors = [n for n in neighbors if 0 <= n.x <= borders.x and 0 <= n.y <= borders.y]
    return neighbors
