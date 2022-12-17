class P(tuple):

  def __add__(self, other):

    return P(x1+x2 for x1,x2 in zip(self, other))

  def __mul__(self, integer):

    return P(x * integer for x in self)

  @property
  def x(self):

    return self[0]

  @property
  def y(self):

    return self[1]

  __rmul__ = __mul__
