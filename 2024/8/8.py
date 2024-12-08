import fileinput
from collections import defaultdict
from itertools import combinations

from P import P

EMPTY = "."

class Map:
  def __init__(self, lines):
    self.antennas = defaultdict(list)
    self.antinodes = set()

    for y, line in enumerate(lines):
      for x, symbol in enumerate(line.strip()):
        if symbol != EMPTY:
          self.antennas[symbol].append(P(x,y))

    self.width = x + 1
    self.height = y + 1

  def __contains__(self, point):
    return (0 <= point.x < self.width and
            0 <= point.y < self.height)

  def find_antinodes(self):
    for coordinates in self.antennas.values():
      for a, b in combinations(coordinates, 2):
        offset = -1 * a + b
        for point in (-1 * offset + a, b + offset):
          if point in self:
            self.antinodes.add(point)

def main():
  area_map = Map(fileinput.input())

  # part 1
  area_map.find_antinodes()
  print(len(area_map.antinodes))

if __name__ == "__main__":
  main()