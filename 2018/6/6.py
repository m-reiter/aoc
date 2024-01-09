#!/usr/bin/python3

import fileinput
from collections import defaultdict

from P import P

SAFE_DISTANCE = 10000

def manhattan(p1,p2):
  return abs(p1.x-p2.x)+abs(p1.y-p2.y)

def read_data():
  coordinates = []
  for line in fileinput.input():
   x,y = map(int,line.split(", "))
   coordinates.append(P(x,y))
  return coordinates

def main():
  coordinates = read_data()
  
  xmin = min(p.x for p in coordinates) - 1
  ymin = min(p.y for p in coordinates) - 1
  xmax = max(p.x for p in coordinates) + 1
  ymax = max(p.y for p in coordinates) + 1

  finite = set(range(len(coordinates)))
  area = defaultdict(int)
  safe = 0

  for x in range(xmin,xmax+1):
    for y in range(ymin,ymax+1):
      distances = [manhattan(P(x,y),p) for p in coordinates]
      if distances.count(min(distances)) == 1:
        nearest = distances.index(min(distances))
        area[nearest] += 1
      if x in (xmin,xmax) or y in (ymin,ymax):
        finite.discard(nearest)
      if sum(distances) < SAFE_DISTANCE:
        safe += 1

  biggest = max(finite,key = lambda x: area[x])
  print(area[biggest])
  print(safe)

if __name__ == "__main__":
  main()
