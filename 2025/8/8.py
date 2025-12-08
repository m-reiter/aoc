#!/usr/bin/python3

import fileinput

from itertools import count, combinations
from functools import reduce
from operator import mul

from P import P

class Junction(P):
  def __new__(cls, *point):
    junction = super().__new__(cls, *point)
    junction.circuit = None
    return junction

  def __repr__(self):
    return f"<Junction{super(P, self).__repr__()}{f' in circuit {self.circuit.id}' if self.circuit else ''}>"

  def connect(self, partner):
    if c := self.circuit:
      return c.add(partner)
    elif c := partner.circuit:
      return c.add(self)
    else:
      Circuit(self, partner)

class Circuit:
  id_generator = count()

  def __init__(self, *junctions):
    self.empty()
    for junction in junctions:
      self.add(junction)
    self.id = next(Circuit.id_generator)

  def __repr__(self):
    return f"<Circuit {self.id} containing {len(self.junctions)} junctions>"

  def empty(self):
    self.junctions = set()

  def __len__(self):
    return len(self.junctions)

  def add(self, junction):
    if junction in self.junctions:
      return
    elif (c := junction.circuit) is not None:
      affected = c.junctions
      c.empty() # shouldn't be necessary (garbage collection) but I'm not sure
    else:
      affected = { junction }
    for j in affected:
      j.circuit = self
      self.junctions.add(j)
    return c

def connect(first, second, circuits):
  empty_circuit = first.connect(second)
  if empty_circuit is None:
    # new circuit was created
    circuits.add(first.circuit)
  else:
    # connect returns empty circuit of 2 circuits are fused
    circuits.remove(empty_circuit)
  
def main():
  junctions = [ Junction(*map(int, line.split(','))) for line in fileinput.input() ]

  distances = sorted((abs(first-second), first, second) for first, second in combinations(junctions, 2))

  # part 1
  n_connections = 10 if len(junctions) < 100 else 1000 # distinguish sample data from real input
  circuits = set()
  for _, first, second in distances[:n_connections]:
    connect(first, second, circuits)

  print(reduce(mul, sorted((len(c) for c in circuits), reverse = True)[:3]))

  # part 2
  for _, first, second in distances[n_connections:]:
    connect(first, second, circuits)
    if len(circuits) == 1:
      if len(c := circuits.pop()) == len(junctions):
        # all junctions are in one single circuit
        break
      else:
        # add popped circuit back
        circuits.add(c)

  print(first.x * second.x)


if __name__ == "__main__":
  main()
