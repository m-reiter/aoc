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
                     start,
                     destination = None,
                     path_to_here = [ P(0,0) ],
                     directions_from_here = (RIGHT, DOWN),
                     heat_loss_to_here = 0):
    if destination == None:
      destination = self.dimension
#    print(start, heat_loss, self.minimum_heat_loss, len(path), self.cache[start])
#    print(start, destination, heat_loss, self.minimum_heat_loss, visited)

    try:
      if heat_loss_to_here >= self.minimum_heat_loss:
        return None
    except TypeError:
      pass

    if start == destination:
      self.minimum_heat_loss = heat_loss_to_here
      self.best_path = path_to_here
      result = heat_loss_to_here
    else:
      try:
        previous_heat_loss, result = self.cache[start][directions_from_here]
      except KeyError:
        pass
      else:
        if previous_heat_loss >= heat_loss_to_here:
          print("***", "cache hit!")
          return result

      candidates = defaultdict(list)

      for direction in directions_from_here:
        new_heat_loss = heat_loss_to_here
        new_directions = TURNS[direction]
        new_path = [ *path_to_here ]
        for steps in range(1, 4):
          candidate = start + direction * steps
          if candidate in self and not candidate in path_to_here:
#            print("*",candidate)
            new_heat_loss += self[candidate]
            new_path = [ *new_path, candidate ]
            candidates[steps].append((candidate, 
                                      destination, 
                                      new_path,
                                      new_directions,
                                      new_heat_loss))
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

    self.cache[start][directions_from_here] = (heat_loss_to_here, result)
    return result

def main():
  #return
  city = City.from_input()
  print(city)
  print()
  print(city.find_best_path(city.start))
  print()
  print(city)
  print(city.best_path)
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
