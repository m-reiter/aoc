#!/usr/bin/python3

import fileinput

from P import P

def is_wall(point,favorite=10):
  x,y = point
  return bin(x*x + 3*x + 2*x*y + y + y*y + favorite).count("1") % 2 == 1

def draw_office(size,favorite=10):
  for y in range(size):
    print("".join("#" if is_wall(P(x,y),favorite) else "." for x in range(size)))

def find_shortest_path(destination,start=P(1,1),favorite=10):
  visited = {start}
  path = 0
  while not destination in visited:
    old = len(visited)
    for p in list(visited):
      for n in p.get_neighbors(diagonals=False,borders=p+P(1,1)):
        if not is_wall(n,favorite):
          visited.add(n)
    if len(visited) == old:
      return -1
    path += 1
    if path == 50:
      reachable = len(visited)
    print(path,len(visited))
  return path, reachable

def main():
  draw_office(40)
  print(find_shortest_path(P(31,39),favorite=1358))

if __name__ == "__main__":
  main()
