#!/usr/bin/python3

import fileinput
import re
from collections import defaultdict
from itertools import chain

FOLDING = re.compile("fold along ([xy])=(\d+)")

def read_paper(data):
  dots = defaultdict(lambda: defaultdict(bool))
  for line in data:
    if not line.strip():
      break
    x,y = map(int,line.split(","))
    dots[x][y] = True
  dimx = max(dots.keys())+1
  dimy = max(chain.from_iterable(x.keys() for x in dots.values()))+1
  return ["".join("#" if dots[x][y] else "." for x in range(dimx)) for y in range(dimy)]

def read_folds(data):
  return [ (direction,int(position)) for direction,position in [ FOLDING.match(line).groups() for line in data ]]

def fold(paper,direction,position):
  dimx = len(paper[0])
  dimy = len(paper)
  if direction == "y":
    newpaper = ["".join("#" if paper[y][x] == "#" or paper[dimy-y-1][x] == "#" else "." for x in range(dimx)) for y in range(position)]
  elif direction == "x":
    paper = [line + "."*100 for line in paper]
#    newpaper = ["".join("#" if paper[y][x] == "#" or paper[y][dimx-x-1] == "#" else "." for x in range(position)) for y in range(dimy)]
    newpaper = ["".join("#" if paper[y][x] == "#" or paper[y][2*position-x] == "#" else "." for x in range(position)) for y in range(dimy)]
  return newpaper


def main():
  data = fileinput.input()
  paper = read_paper(data)

  folds = read_folds(data)

  firstfold = direction,position = folds.pop(0)

  paper = fold(paper,direction,position)

  print(sum(line.count("#") for line in paper))

  for direction,position in folds:
    paper = fold(paper,direction,position)

  print("\n".join(paper))


if __name__ == "__main__":
  main()
