#!/usr/bin/python3

import fileinput
from collections import defaultdict, deque

from P import P

class MemorySpace:
  def __init__(self, bytes, size = 70):
    self.bytes = bytes
    self.size = size

  def is_free(self, position, nanoseconds):
    return position not in self.bytes[:nanoseconds]
    
  def find_path(self, nanoseconds):
    destination = P(self.size, self.size)
    paths = deque([ [ P(0, 0) ] ])
    visited = set()

    while paths:
      current = paths.popleft()
      for neighbor in current[-1].get_neighbors(diagonals = False, borders = P(self.size, self.size)):
        if neighbor not in visited and self.is_free(neighbor, nanoseconds):
          visited.add(neighbor)
          new_path = current + [ neighbor ]
          if neighbor == destination:
            return new_path
          paths.append(new_path)

def main():
  input_lines = list(fileinput.input())
  size = 70 if len(input_lines) > 50 else 6
  nanoseconds = 1024 if len(input_lines) > 50 else 12

  bytes = [ P(*map(int, line.strip().split(","))) for line in input_lines ]
  memoryspace = MemorySpace(bytes, size = size)

  # part 1
  path = memoryspace.find_path(nanoseconds)
  print(len(path) - 1)

  # part 2
  for nanoseconds in range(len(bytes) + 1):
    if memoryspace.find_path(nanoseconds) is None:
      break
  print(bytes[nanoseconds - 1])

if __name__ == "__main__":
  main()
