#!/usr/bin/python3

import fileinput
import re
from itertools import groupby

PARTICLE = re.compile("p=<(.*)>, v=<(.*)>, a=<(.*)>")

def manhattan(value):
  return sum(map(abs,value))

class Particle():
  def __init__(self,p,v,a):
    self.p = p
    self.v = v
    self.a = a

  def __repr__(self):
    return "<p={}, v={}, a={}>".format(self.p,self.v,self.a)

  def move(self):
    self.v = tuple(vi+ai for vi,ai in zip(self.v,self.a))
    self.p = tuple(pi+vi for pi,vi in zip(self.p,self.v))

def read_input():
  particles = []
  for line in fileinput.input():
    groups = PARTICLE.match(line).groups()
    p,v,a = (tuple(map(int,group.split(","))) for group in groups)
    particles.append(Particle(p,v,a))
  return particles

def main():
  particles = read_input()
  nearest = min(particles, key=lambda x: manhattan(x.a))
  print(particles.index(nearest))

  p = lambda x: x.p
  for _ in range(1000):
    particles.sort(key=p)
    remaining = []
    for position,occupants in groupby(particles,p):
      occupants = list(occupants)
      if len(occupants) == 1:
        remaining.extend(occupants)
    particles = remaining
    for particle in particles:
      particle.move()
    
  print(len(particles))
    
if __name__ == "__main__":
  main()
