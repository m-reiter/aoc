#!/usr/bin/python3

import fileinput
from collections import defaultdict

from P import P

OUTSIDE = "."

class Garden:
  def __init__(self, lines):
    self.plots = defaultdict(lambda: OUTSIDE)

    for y, line in enumerate(lines):
      for x, plant in enumerate(line.strip()):
        self.plots[P(x,y)] = plant

    self.borders = P(x,y)
    self.regions = []

  def find_regions(self):
    unhandled = set(self.plots)

    while unhandled:
#      print(unhandled)
      area = set()
      perimeter = 0
      seed = unhandled.pop()
      plant = self.plots[seed]
      new = { seed }
      while new:
#        print(new)
        plot = new.pop()
        area.add(plot)
        for neighbor in plot.get_neighbors(diagonals = False):
          if self.plots[neighbor] == plant:
            if neighbor not in area:
              new.add(neighbor)
              unhandled.discard(neighbor)
          else:
            perimeter += 1
      self.regions.append((area, perimeter))

def main():
  garden = Garden(fileinput.input())
  
  garden.find_regions()
#  for region, perimeter in garden.regions:
#    print(f"size {len(region)}, perimeter {perimeter}")
  print(sum(len(region) * perimeter for region, perimeter in garden.regions))

if __name__ == "__main__":
  main()
