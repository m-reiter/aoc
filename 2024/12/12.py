#!/usr/bin/python3

import fileinput
from collections import defaultdict

from P import P

OUTSIDE = "."

UP    = P( 0, -1)
DOWN  = P( 0,  1)
LEFT  = P(-1,  0)
RIGHT = P( 1,  0)

LATERALS = {
  UP:    (LEFT, RIGHT),
  DOWN:  (LEFT, RIGHT),
  LEFT:  (UP, DOWN),
  RIGHT: (UP, DOWN)
}

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
      area = set()
      perimeter = 0
      sides = 0
      side_segments = set()
      seed = unhandled.pop()
      plant = self.plots[seed]
      new = { seed }
      while new:
        plot = new.pop()
        area.add(plot)
        for neighbor in plot.get_neighbors(diagonals = False):
          if self.plots[neighbor] == plant:
            if neighbor not in area:
              new.add(neighbor)
              unhandled.discard(neighbor)
          else:
            perimeter += 1
            if (plot, neighbor) not in side_segments:
              sides += 1
              side_segments.add((plot, neighbor))
              for direction in LATERALS[neighbor - plot]:
                offset = 1
                while (self.plots[(p:= plot + offset * direction)] == plant
                       and self.plots[(n := neighbor + offset * direction)] != plant):
                  side_segments.add((p, n))
                  offset += 1
      self.regions.append((area, perimeter, sides))

def main():
  garden = Garden(fileinput.input())
  
  garden.find_regions()

  # part 1
  print(sum(len(region) * perimeter for region, perimeter, sides in garden.regions))

  # part 2
  print(sum(len(region) * sides for region, perimeter, sides in garden.regions))

if __name__ == "__main__":
  main()
