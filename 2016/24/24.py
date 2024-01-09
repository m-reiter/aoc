#!/usr/bin/python3

import fileinput
from itertools import permutations
from more_itertools import pairwise

from P import P

WALL = "#"

def read_input():
  walls = set()
  targets = {}
  for y,line in enumerate(fileinput.input()):
    for x,char in enumerate(line.strip()):
      if char.isnumeric():
        targets[P(x,y)] = char
      elif char == WALL:
        walls.add(P(x,y))
  return walls,targets

def find_shortest_paths(walls,targets,tier=0):
  if len(targets) < 2:
    return {}
  shortest_paths = {}
  targets = targets.copy()
  start,label = targets.popitem()
  current = visited = { start, }
  steps = 0
  while len(shortest_paths) < 2*len(targets):
    steps += 1
    candidates = { p for position in current for p in position.get_neighbors(diagonals=False) if p not in walls and p not in visited }
    for candidate in candidates:
      if candidate in targets:
        shortest_paths[(label,targets[candidate])] = shortest_paths[(targets[candidate],label)] = steps
    visited |= candidates
    current = candidates
  remainder = find_shortest_paths(walls,targets,tier+1)
  shortest_paths.update(remainder)
  return shortest_paths
  #.update(find_shortest_paths(walls,targets,tier+1))
  
def part1(walls,targets,shortest_paths,start="0"):
  lengths = {}
  stations = [ v for v in targets.values() if v != start ]
  for order in permutations(stations):
    lengths[order] = sum(shortest_paths[pair] for pair in pairwise((start,)+order))
  return min(lengths.values())

def part2(walls,targets,shortest_paths,start="0"):
  lengths = {}
  stations = [ v for v in targets.values() if v != start ]
  for order in permutations(stations):
    lengths[order] = sum(shortest_paths[pair] for pair in pairwise((start,)+order+(start,)))
  return min(lengths.values())

def main():
  walls,targets = read_input()
  shortest_paths = find_shortest_paths(walls,targets)
  print(part1(walls,targets,shortest_paths))
  print(part2(walls,targets,shortest_paths))

if __name__ == "__main__":
  main()
