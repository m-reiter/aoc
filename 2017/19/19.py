#!/usr/bin/python3

import fileinput
import string
from collections import defaultdict

from P import P

CORNER = "+"
WALLS = "|-"
EMPTY = ""

def read_input():
  diagram = defaultdict(str)
  corners = []
  for y,line in enumerate(fileinput.input()):
    if y == 0:
      start = P(line.index("|"),0)
    for x,char in enumerate(line.strip("\n")):
      if char.strip() != EMPTY:
        diagram[P(x,y)] = char
        if char == CORNER:
          corners.append(P(x,y))
  assert all(sum(diagram[p] != EMPTY for p in corner.get_neighbors(diagonals=False)) == 2 for corner in corners)
  return diagram,start

def navigate(diagram,start):
  # part 1
  letters = []
  pos = start
  direction = P(0,1)
  steps = 0

  while True:
    while diagram[pos] != CORNER:
      current = diagram[pos]
      if current == EMPTY:
        return letters,steps
      elif current in string.ascii_uppercase:
        letters.append(current)
      pos += direction
      steps += 1
    direction = P(*reversed(direction))
    if diagram[pos+direction] == EMPTY:
      direction *= -1
    pos += direction
    steps += 1

def main():
  diagram,start = read_input()
  letters,steps = navigate(diagram,start)
  print("".join(letters))
  print(steps)

if __name__ == "__main__":
  main()
  pass
