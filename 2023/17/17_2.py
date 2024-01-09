#!/usr/bin/python3

import fileinput

from collections import defaultdict
from more_itertools import pairwise
from termcolor import colored

from P import P

UP = P(0, -1)
DOWN = P(0, 1)
LEFT = P(-1, 0)
RIGHT = P(1, 0)

PRINTCHARS = {
  UP: "^",
  DOWN: "v",
  LEFT: "<",
  RIGHT: ">"
}

TURNS = {
  UP: (RIGHT, LEFT),
  DOWN: (RIGHT, LEFT),
  RIGHT: (DOWN, UP),
  LEFT: (DOWN, UP)
}

class City(dict):
  def __init__(self, *args, **kwargs):
    super().__init__(*args, **kwargs)
    self.dimension = None
    self.minimum_heat_loss = 1000000000
#    self.minimum_heat_loss = 103
    self.best_path = []
    self.start = P(0,0)
    self.caches = defaultdict(dict)
    self.crucible = (4,11)
  
  def __str__(self):
    replacements = { second: colored(PRINTCHARS[second - first], "red") for first, second in pairwise(self.best_path) }

    return "\n".join(
      "".join(replacements[P(x, y)] if P(x, y) in  replacements else str(self[x, y]) for x in range(self.dimension.x + 1))
      for y in range(self.dimension.y + 1)
    )
    
  @classmethod
  def from_input(cls):
    city = cls()
    
    for y, line in enumerate(fileinput.input()):
      for x, heat in enumerate(line.strip()):
        city[x, y] = int(heat)
    
    city.dimension = P(x, y)

    return city
  
#  def __getitem__(self, key):
#    key = P(*key)
#    
#    if not 0 <= key.x <= self.dimension.x and 0 <= key.y <= self.dimension.y:
#      return -1
#    
#    return super().__getitem__(key)
  
  def find_paths(self,
                 start = None,
                 destination = None,
                 visited = [ P(0, 0) ],
                 directions = (RIGHT, DOWN),
                 heat_loss = 0):
    if start == None:
      start = self.start
    if destination == None:
      destination = self.dimension
#    print(start, destination, heat_loss, self.minimum_heat_loss, len(history))
#    print(start, destination, heat_loss, self.minimum_heat_loss, visited)

    previous = self.caches[start].get(directions, None)
    if previous and heat_loss >= previous:
      return
    self.caches[start][directions] = heat_loss

    candidates = defaultdict(list)

    for direction in directions:
      new_heat_loss = heat_loss
      new_directions = TURNS[direction]
      new_visited = visited
      for steps in range(1, self.crucible[1]):
        candidate = start + direction * steps
        if candidate in self and not candidate in visited:
          new_heat_loss += self[candidate]
          if new_heat_loss >= self.minimum_heat_loss:
            break
          new_visited = new_visited + [ candidate ]
          if candidate == destination:
              self.minimum_heat_loss = new_heat_loss
              self.best_path = new_visited
          elif steps >= self.crucible[0]:
            candidates[steps].append((candidate, 
                                      destination, 
                                      new_visited,
                                      new_directions,
                                      new_heat_loss))

    for steps in sorted(candidates.keys(), reverse = True):
      for candidate in candidates[steps]:
        self.find_paths(*candidate)

def main():
#  return
  city = City.from_input()

  # part 1
  print(city)
  print()
  city.find_paths()
  print()
  print(city.minimum_heat_loss)
  print(city.best_path)
  print()
  print(city)

if __name__ == "__main__":
  main()
