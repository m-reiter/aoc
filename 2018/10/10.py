#!/usr/bin/python3

import fileinput
import re

from P import P

POINT = re.compile("position=<(\s*-*\d+), (\s*-*\d+)> velocity=<(\s*-*\d+), (\s*-*\d+)>")

def print_points(points):
  coords = [p[0] for p in points]
  xmin = min(p.x for p in coords)
  xmax = max(p.x for p in coords)
  ymin = min(p.y for p in coords)
  ymax = max(p.y for p in coords)

  for y in range(ymin,ymax+1):
    print("".join("#" if P(x,y) in coords else "." for x in range(xmin,xmax+1)))

  return ymax-ymin

def main():
  points = [ list(map(int,POINT.match(line).groups())) for line in fileinput.input() ]
  points = [[P(*p[:2]),P(*p[2:])] for p in points]

  seconds = 0

  while True:
    seconds += 1
    ymin,ymax = 10000,-10000
    for point in points:
      point[0] = point[0] + point[1]
      ymin = min(ymin,point[0].y)
      ymax = max(ymax,point[0].y)
    if ymax-ymin <= 9:
      break

  print_points(points)
  print(seconds)

if __name__ == "__main__":
  main()
