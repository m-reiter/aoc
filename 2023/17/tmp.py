#!/usr/bin/python3

import fileinput

from collections import defaultdict
from more_itertools import pairwise

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
    self.minimum_heat_loss = None
#    self.minimum_heat_loss = 103
    self.cache = defaultdict(dict)
    self.best_path = []
    self.start = P(0,0)
  
  def __str__(self):
    replacements = { second: PRINTCHARS[second - first] for first, second in pairwise(self.best_path) }

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
  
  def find_best_path(self,
                     start = None,
                     destination = None,
                     path = [],
                     directions = (RIGHT, DOWN),
                     heat_loss = 0):
    if start == None:
      start = self.start
    if destination == None:
      destination = self.dimension
    print(start, heat_loss, self.minimum_heat_loss, len(path), self.cache[start])
#    print(start, destination, heat_loss, self.minimum_heat_loss, visited)

    if self.minimum_heat_loss and heat_loss >= self.minimum_heat_loss:
      return None

    if start == destination:
      self.minimum_heat_loss = heat_loss
      self.best_path = path
      result = heat_loss
    else:
      try:
        previous_heat_loss, best_path = self.cache[start][tuple(sorted(directions))]
      except KeyError:
        pass
      else:
        if previous_heat_loss >= heat_loss:
          print("***", "cache hit!")
          return best_path

      candidates = defaultdict(list)

      for direction in directions:
        new_heat_loss = heat_loss
        new_directions = TURNS[direction]
        new_path = [ *path, start ]
        for steps in range(1, 4):
          candidate = start + direction * steps
          if candidate in self and not candidate in path:
#            print("*",candidate)
            new_heat_loss += self[candidate]
            candidates[steps].append((candidate, 
                                      destination, 
                                      new_path,
                                      new_directions,
                                      new_heat_loss))
            new_path = [ *new_path, candidate ]
          else:
            break

      print("*",candidates)
      losses = [ self.find_best_path(*candidate)
                 for steps in sorted(candidates.keys(), reverse = True)
                 for candidate in candidates[steps]
               ]
      try:
        result = min(loss for loss in losses if loss is not None)
      except ValueError:
        result = None

    self.cache[start][tuple(sorted(directions))] = (heat_loss, result)
    return result

def main():
  #return
  city = City.from_input()
  print(city)
  print()
  print(city.find_best_path())
  return

  # part 1
  print(city)
  print()
  city.find_paths()
  print(city)
  print()
  print(city.minimum_heat_loss)
  print(city.best_path)

if __name__ == "__main__":
  main()
