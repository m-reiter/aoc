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

DISTANCE_TO_START = {
  ">": 0,
  "^": 1,
  "v": 2,
  "<": 3
}

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

    self.paths = { (pad, pad): "" for pad in self.keys() }
    paths = defaultdict(set)
    for (first, p1), (second, p2) in permutations(self.items(), 2):
      horizontal_first = P(p2.x, p1.y) != self.gap
      vertical_first = P(p1.x, p2.y) != self.gap
      difference = p2 - p1
      steps_x = HORIZONTAL[sign(difference.x)] * abs(difference.x)
      steps_y = VERTICAL[sign(difference.y)] * abs(difference.y)
      if horizontal_first:
        paths[(first, second)].add(steps_x + steps_y)
      if vertical_first:
        paths[(first, second)].add(steps_y + steps_x)
    self.paths.update({ key: min(path, key = lambda x: DISTANCE_TO_START[x[0]]) for key, path in paths.items() })

    self.controller = None
    self.current = "A"

  def presses(self, combination):
    presses = "".join(self.paths[(a, b)] + "A" for a, b in pairwise("A" + combination))
    print(presses)
    if self.controller is None:
      return len(presses)
    else:
      return self.controller.presses(presses)
    
  def dummy():
    path = list(self.paths[(self.current, target)])[0] + "A"
    if self.controller is None:
      presses = len(path)
    else:
      presses = sum(self.controller.presses(next_step) for next_step in path)
    self.current = target
    return presses

  def shortest_path_length(self, combination, top_level = False):
    breakpoint()
    if top_level:
      segments = [ [ path + "A" for path in self.paths[a, b] ] for a, b in pairwise("A" + combination) ]
      paths = { "".join(sequence) for sequence in product(*segments) }
      #path = min(paths, key = lambda x: DISTANCE_TO_START[x[0]])
      #print(path, paths)
      return min([self.controller.shortest_path_length(path) for path in paths])
    else:
      return sum(self.controller.presses(next_step) for next_step in combination)
      path = "".join(list(self.paths[(a,b)])[0] + "A" for a, b in pairwise("A" + combination)) 
      if self.controller is None:
        return len(path)
      else:
        length = 0
        for a, b in pairwise(path):
          length += self.controller.shortest_path_length(a+b)
        return length

  def complexity(self, code):
    shortest = self.presses(code)
    print(code, shortest, int(code[:-1]))
    return shortest * int(code[:-1])

def main():
  decimal = Layout(DECIMAL)
  decimal.controller = Layout(DIRECTIONAL)
  latest = decimal.controller.controller = Layout(DIRECTIONAL)

  codes = list(map(str.strip, fileinput.input()))

  # part 1
  print(sum(map(decimal.complexity, codes)))

  # part 2
  for _ in range(23):
    new = Layout(DIRECTIONAL)
    latest.controller = new
    latest = new
  #breakpoint()

if __name__ == "__main__":
  main()
