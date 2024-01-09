#!/usr/bin/python3

import fileinput
import re

CLAIM = re.compile("#(\d+) @ (\d+),(\d+): (\d+)x(\d+)")

def main():
  claims = [tuple(map(int,CLAIM.match(line.strip()).groups())) for line in fileinput.input()]
  
  # part 1
  used = set()
  double = set()

  for ID,startx,starty,width,height in claims:
    for x in range(startx,startx+width):
      for y in range(starty,starty+height):
        if (x,y) in used:
          double.add((x,y))
        else:
          used.add((x,y))

  print(len(double))

  #part 2
  for ID,startx,starty,width,height in claims:
    if any((x,y) in double for x in range(startx,startx+width) for y in range(starty,starty+height)):
      continue
    print(ID)
    break

if __name__ == "__main__":
  main()
