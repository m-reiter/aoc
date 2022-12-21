#!/usr/bin/python3

import fileinput

def part1(cubes):
  covered_sides = []
  for cube in cubes:
    covered = 0
    for coord in range(3):
      neighbour = list(cube)
      for x in range(cube[coord]-1,cube[coord]+2,2):
        neighbour[coord] = x
        if tuple(neighbour) in cubes:
          covered += 1
    covered_sides.append(covered)
  return 6*len(cubes)-sum(covered_sides)

def get_shell(lowest,highest):
  shell = [(x,y,z)
           for x in range(lowest[0]-1,highest[0]+2)
           for y in range(lowest[1]-1,highest[1]+2)
           for z in range(lowest[2]-1,highest[2]+2)
           if x == lowest[0]-1 or x == highest[0]+1
           or y == lowest[1]-1 or y == highest[1]+1
           or z == lowest[2]-1 or z == highest[2]+1]
  return shell 

def seep(oozing,next_layer,cubes):
  seeped = True
  while seeped:
    seeped = False
    candidates = [point for point in next_layer if point not in oozing and point not in cubes]
    for x,y,z in candidates:
      if ((x-1,y,z) in oozing or (x+1,y,z) in oozing or
          (x,y-1,z) in oozing or (x,y+1,z) in oozing or
          (x,y,z-1) in oozing or (x,y,z+1) in oozing):
        oozing.append((x,y,z))
        seeped = True
  return oozing

def ooze_in(oozed,lowest,highest,cubes):
  ranges = zip(lowest,highest)
  shrunk = False
  for coord,range in enumerate(ranges):
    if range[1]-range[0] >= 2:
      lowest[coord] += 1
      highest[coord] -= 1
      shrunk = True
  next_layer = get_shell(lowest,highest)
  oozing = [(x,y,z) for x,y,z in next_layer
            if (x,y,z) not in cubes and
            ((x-1,y,z) in oozed or (x+1,y,z) in oozed or
             (x,y-1,z) in oozed or (x,y+1,z) in oozed or
             (x,y,z-1) in oozed or (x,y,z+1) in oozed)]
  oozing = seep(oozing,next_layer,cubes)
  return oozed + oozing, shrunk, lowest, highest

def part2(cubes):
  covered_sides = []
  lowest = [min(cube[coord] for cube in cubes) for coord in range(3)]
  highest = [max(cube[coord] for cube in cubes) for coord in range(3)]
  oozed = get_shell(lowest,highest)
  shrunk = True
  while shrunk:
    oozed,shrunk,lowest,highest = ooze_in(oozed,lowest,highest,cubes)
  for cube in cubes:
    covered = 0
    for coord in range(3):
      neighbour = list(cube)
      for x in range(cube[coord]-1,cube[coord]+2,2):
        neighbour[coord] = x
        if tuple(neighbour) in cubes or tuple(neighbour) not in oozed:
          covered += 1
    covered_sides.append(covered)
  return 6*len(cubes)-sum(covered_sides)

def main():
  cubes = [tuple(map(int,line.split(","))) for line in fileinput.input()]
  print(part1(cubes))
  print(part2(cubes))

if __name__ == "__main__":
  main()
