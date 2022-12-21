#!/usr/bin/python3

import fileinput

KEY = 811589153

def mix(coordinates, times = 1):
  length = len(coordinates)
  indices = list(range(length))
  for _ in range(times):
    for original_position,coordinate in enumerate(coordinates):
      current_position = indices.index(original_position)
      indices.pop(current_position)
      new_position = (current_position + coordinate) % (length - 1)
      indices = indices[:new_position]+[original_position]+indices[new_position:]
  mixed = [coordinates[index] for index in indices]
  return mixed
  
def get_coords(mixed):
  zero = mixed.index(0)
  return [mixed[(zero + i*1000) % len(mixed)] for i in (1,2,3)]

def part1(coordinates):
  mixed = mix(coordinates)
  return sum(get_coords(mixed))

def part2(coordinates):
  coordinates = [coord * KEY for coord in coordinates]
  mixed = mix(coordinates,times = 10)
  return sum(get_coords(mixed))

def main():
  coordinates = list(map(int,fileinput.input()))

  print(part1(coordinates))
  print(part2(coordinates))

if __name__ == "__main__":
  main()
