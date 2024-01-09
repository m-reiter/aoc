#!/usr/bin/python3

import fileinput
from P import P
from numpy import sign

OFFSETS = {
  'n':  P(0,2),
  's':  P(0,-2),
  'nw': P(-1,1),
  'ne': P(1,1),
  'sw': P(-1,-1),
  'se': P(1,-1)
}

def calculate_distance(position):
  distance = min(abs(coord) for coord in position)
  position -= distance * P(sign(position.x),sign(position.y))
  if position.x == 0:
    return distance + abs(position.y) // 2
  return distance + abs(position.x)

def main():
  paths = [ line.strip() for line in fileinput.input() ]

  for path in paths:
    max_distance = 0
    position = P(0,0)
    for direction in path.split(','):
      position += OFFSETS[direction]
      distance = calculate_distance(position)
      if distance > max_distance:
        max_distance = distance
        max_position = position
    print(path)
    print(distance)
    print(position)
    print(max_distance)
    print(max_position)

if __name__ == "__main__":
  main()
