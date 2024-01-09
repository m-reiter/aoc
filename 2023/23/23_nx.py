#!/usr/bin/python3

import fileinput
import networkx as nx

from attr import attrs, attrib
from termcolor import colored
from collections import deque
from more_itertools import pairwise

from P import P

FOREST = colored("#", "green")
PATH= "."

FANCY = { PATH: "O" }

NORTH = P(0, -1)
SOUTH = P(0, 1)
WEST = P(-1, 0)
EAST = P(1, 0)

SLOPES = {
  "^": NORTH,
  "v": SOUTH,
  "<": WEST,
  ">": EAST
}

@attrs
class Map:
  paths = attrib(factory = list)
  slopes = attrib(factory = dict)
  start = attrib(default = None)
  destination = attrib(default = None)
  size = attrib(default = None)
  hikes = attrib(factory = list)
  graph = attrib(factory = nx.DiGraph)
  edges = attrib(factory = dict)

  def __getitem__(self, key):
    if key in self.slopes:
      return self.slopes[key]
    elif key in self.paths:
      return PATH
    else:
      return FOREST

  def __contains__(self, point):
    return point in list(self.slopes.keys()) + self.paths

  def __str__(self):
    return "\n".join(
      "".join(self[P(x, y)] for x in range(self.size.x))
      for y in range(self.size.y)
    )

  @classmethod
  def from_input(cls):
    paths = []
    slopes = {}

    for y, line in enumerate(fileinput.input()):
      for x, char in enumerate(line.strip()):
        if char == PATH:
          paths.append(P(x, y))
          if y == 0:
            start = P(x, y)
          else:
            destination = P(x, y)
        elif char in SLOPES:
          slopes[P(x, y)] = char

    return cls(paths, slopes, start, destination, P(x + 1, y + 1))

  def analyse(self):
    nodes = [ self.start, self.destination ]

    nodes.extend(node for node in self.paths if sum(n in self for n in node.get_neighbors(diagonals = False)) > 2)

    for node in nodes:
      strolls = deque([[ node ]])

      while strolls:
        stroll = strolls.popleft()
        current_position = stroll[-1]
        if current_position != node and current_position in nodes:
          self.graph.add_edge(node, current_position, weight = len(stroll) - 1)
          self.edges[node, current_position] = stroll
          continue
        if current_position in self.paths:
          next_steps = [ p for p in current_position.get_neighbors(diagonals = False) if p in self and not p in stroll ]
        else: # on slope
          next_steps = [ current_position + SLOPES[self[current_position]] ]
          if next_steps[0] in stroll:
            continue
        strolls.extend(stroll + [ step ] for step in next_steps)

    return nodes

  def path_length(self, path):
    return sum(self.graph[first][second]["weight"] for first, second in pairwise(path))

  def flatten(self):
    for first, second in list(self.edges.keys()):
      if not (second, first) in self.edges:
        self.edges[second, first] = self.edges[first, second]
        self.graph.add_edge(second, first, weight = self.graph[first][second]["weight"])

  def find_longest_hike(self):
    
    hikes = list(nx.all_simple_paths(self.graph, self.start, self.destination))
    
    longest_hike = max(hikes, key = self.path_length)

    self.longest_hike = longest_hike

  def print_hike(self):
    hike = [ self.start ]

    for first, second in pairwise(self.longest_hike):
      hike.extend(self.edges[first, second])

    for y in range(self.size.y):
      for x in range(self.size.x):
        field = self[P(x, y)]
        print(colored(FANCY.get(field, field), "red") if P(x, y) in hike else field, end = "")
      print()
    
def main():
  map = Map.from_input()
  print(map)
  print()

  # part 1
  map.analyse()
  map.find_longest_hike()

  map.print_hike()
  print()
  print(map.path_length(map.longest_hike))
  print()

  # part 2
  map.flatten()
  
  map.find_longest_hike()

  map.print_hike()
  print()
  print(map.path_length(map.longest_hike))

if __name__ == "__main__":
  main()
