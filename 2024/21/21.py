#!/usr/bin/python3

import fileinput
from itertools import permutations, product
from more_itertools import pairwise
from collections import defaultdict

from P import P

DECIMAL = [
  "789",
  "456",
  "123",
  " 0A"
]

DIRECTIONAL = [
  " ^A",
  "<v>"
]

GAP = " "

HORIZONTAL = {
  -1: "<",
   1: ">"
}
VERTICAL = {
  -1: "^",
   1: "v"
}

def sign(x):
  return 1 if x > 0 else -1

class Layout(dict):
  def __init__(self, layout):
    for y, line in enumerate(layout):
      for x, char in enumerate(line):
        if char == GAP:
          self.gap = P(x, y)
        else:
          self[char] = P(x, y)

    self.paths = defaultdict(set)
    for pad in self.keys():
      self.paths[(pad, pad)] = { "" }
    for (first, p1), (second, p2) in permutations(self.items(), 2):
      horizontal_first = P(p2.x, p1.y) != self.gap
      vertical_first = P(p1.x, p2.y) != self.gap
      difference = p2 - p1
      steps_x = HORIZONTAL[sign(difference.x)] * abs(difference.x)
      steps_y = VERTICAL[sign(difference.y)] * abs(difference.y)
      if horizontal_first:
        self.paths[(first, second)].add(steps_x + steps_y)
      if vertical_first:
        self.paths[(first, second)].add(steps_y + steps_x)

    self.controller = None

  def find_paths(self, combination):
    segments = [ [ path + "A" for path in self.paths[a, b] ] for a, b in pairwise("A" + combination) ]
    paths = { "".join(sequence) for sequence in product(*segments) }
    if self.controller is None:
      return paths
    else:
      full_paths = set()
      for path in paths:
        full_paths |= self.controller.find_paths(path)
      return full_paths

  def complexity(self, code):
    shortest = len(min(self.find_paths(code), key = len))
    #print(code, shortest, int(code[:-1]))
    return shortest * int(code[:-1])

def main():
  decimal = Layout(DECIMAL)
  decimal.controller = Layout(DIRECTIONAL)
  decimal.controller.controller = Layout(DIRECTIONAL)

  codes = list(map(str.strip, fileinput.input()))

  # part 1
  print(sum(map(decimal.complexity, codes)))

if __name__ == "__main__":
  main()
