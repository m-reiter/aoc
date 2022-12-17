#!/usr/bin/python3

import fileinput
from collections import defaultdict

LEFT = 0
RIGHT = 1
TOP = 2
BOTTOM = 3

def calc_heights(trees):
  heights = {
    LEFT: defaultdict(lambda: defaultdict(int)),
    RIGHT: defaultdict(lambda: defaultdict(int)),
    TOP: defaultdict(lambda: defaultdict(int)),
    BOTTOM: defaultdict(lambda: defaultdict(int))
  }

  for y,line in enumerate(trees):
    height = -1
    for x,tree in enumerate(line):
      heights[LEFT][x][y] = height
      if tree > height:
        height = tree
    height = -1
    for x in range(len(line)-1,-1,-1):
      heights[RIGHT][x][y] = height
      if trees[y][x] > height:
        height = trees[y][x]
  for x in range(len(trees[0])):
    height = -1
    for y in range(len(trees)):
      heights[TOP][x][y] = height
      if trees[y][x] > height:
        height = trees[y][x]
    height = -1
    for y in range(len(trees)-1,-1,-1):
      heights[BOTTOM][x][y] = height
      if trees[y][x] > height:
        height = trees[y][x]

  return heights

def part1(trees,heights):
  return sum(
    1 for x in range(len(trees[0])) for y in range(len(trees)) if any(trees[y][x] > heights[DIR][x][y] for DIR in [LEFT,RIGHT,TOP,BOTTOM])
  )

def part2(trees):
  xdim = len(trees[0])
  ydim = len(trees)
  bestview = (-1,0,0)
  for x in range(xdim):
    for y in range(ydim):
      xtmp = x
      left = 0
      while xtmp > 0 and trees[y][xtmp-1] < trees[y][x]:
        xtmp -= 1
        left += 1
      if xtmp > 0:
        left += 1
      xtmp = x
      right = 0
      while xtmp < xdim-1 and trees[y][xtmp+1]  < trees[y][x]:
        xtmp += 1
        right += 1
      if xtmp < xdim-1:
        right += 1
      ytmp = y
      top = 0
      while ytmp > 0 and trees[ytmp-1][x] < trees[y][x]:
        ytmp -= 1
        top += 1
      if ytmp > 0:
        top += 1
      ytmp = y
      bottom = 0
      while ytmp < ydim-1 and trees[ytmp+1][x]  < trees[y][x]:
        ytmp += 1
        bottom += 1
      if ytmp < ydim-1:
        bottom += 1
      scenic = left*right*top*bottom
      if scenic > bestview[0]:
        bestview = (scenic,x,y)
  return bestview
  
def main():
  trees = [list(map(int,line.strip())) for line in fileinput.input()]
  heights = calc_heights(trees)

  print(part1(trees,heights))
  print(part2(trees))

if __name__ == "__main__":
  main()
