#!/usr/bin/python3

import fileinput

from P import P

def read_input():
  height_map = {}
  for y,line in enumerate(fileinput.input()):
    for x,height in enumerate(line.strip()):
      if height == "S":
        S = P(x,y)
        height = "a"
      elif height == "E":
        E = P(x,y)
        height = "z"
      height_map[P(x,y)] = ord(height)
  borders = P(x,y)
  return height_map,S,E,borders

def step(paths,visited,height_map,borders):
  new_paths = []
  for path in paths:
    for neighbor in path[-1].get_neighbors(diagonals=False,borders=borders):
      if (not neighbor in path and 
          not neighbor in visited and
          height_map[neighbor] - height_map[path[-1]] <= 1):
        visited.append(neighbor)
        new_paths.append(path + [neighbor])
  return new_paths,visited

def solve_part(starting_points,height_map,S,E,borders):
  paths = [[point] for point in starting_points]
  visited = starting_points
  while not E in [path[-1] for path in paths]:
    paths,visited = step(paths,visited,height_map,borders)
  return len(paths[0])-1

def part1(height_map,S,E,borders):
  starting_points = [S]
  return solve_part(starting_points,height_map,S,E,borders)

def part2(height_map,S,E,borders):
  starting_points = [location for location,height in height_map.items() if height == ord("a")]
  return solve_part(starting_points,height_map,S,E,borders)

def main():
  height_map,S,E,borders = read_input()

  print(part1(height_map,S,E,borders))
  print(part2(height_map,S,E,borders))

if __name__ == "__main__":
  main()
