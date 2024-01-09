#!/usr/bin/python3

import fileinput
import re

from itertools import permutations
from more_itertools import pairwise

DISTANCE = re.compile("(\w+) to (\w+) = (\d+)")

def read_input():
  distances = {}
  locations = set()

  for line in fileinput.input():
    source, destination, distance = DISTANCE.match(line.strip()).groups()
    source, destination = sorted((source, destination))
    locations.add(source)
    locations.add(destination)
    distances[(source,destination)] = int(distance)

  return locations, distances

def main():
  locations, distances = read_input()

  shortest = max(distances.values()) * len(locations)
  longest = 0

  for route in permutations(locations):
    length = sum(distances[tuple(sorted((a,b)))] for a,b in pairwise(route))
    if length < shortest:
      shortest = length
      shortest_route = route
    if length > longest:
      longest = length
      longest_route = route

  print(shortest_route)
  print(shortest)

  print(longest_route)
  print(longest)

if __name__ == "__main__":
  main()
