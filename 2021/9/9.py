#!/usr/bin/python3

import fileinput

from operator import mul
from functools import reduce

from P import P

class Heightmap(dict):
  @classmethod
  def from_input(cls):
    heightmap = cls()

    for y, line in enumerate(fileinput.input()):
      for x, digit in enumerate(line.strip()):
        heightmap[P(x,y)] = int(digit)

    heightmap.borders = P(x,y)

    return heightmap

  def find_low_points(self):
    low_points = []

    for position, height in self.items():
      neighbors = position.get_neighbors(diagonals = False, borders = self.borders)
      if all(self[neighbor] > height for neighbor in neighbors):
        low_points.append(position)

    return low_points

  def find_basins(self):
    basins = []

    for low_point in self.find_low_points():
      basin = new_points = [ low_point ]
      while True:
        new_points = set(neighbor
                         for point in new_points
                         for neighbor in point.get_neighbors(diagonals= False, borders = self.borders)
                         if self[neighbor] != 9 and not neighbor in basin)
        if not new_points:
          break
        
        basin.extend(new_points)

      basins.append(basin)

    return basins

def main():
  heightmap = Heightmap.from_input()

  # part 1
  low_points = heightmap.find_low_points()

  print(sum(heightmap[position] + 1 for position in low_points))

  # part 2
  basins = heightmap.find_basins()
  print(reduce(mul, sorted([len(basin) for basin in basins], reverse = True)[:3]))

if __name__ == "__main__":
  main()
