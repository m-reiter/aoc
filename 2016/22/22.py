#!/usr/bin/python3

import fileinput
import re
from itertools import permutations

PATTERN = re.compile("/dev/grid/node-x(\d+)-y(\d+)\s+(\d+)T\s+(\d+)T\s+(\d+)T\s+(\d+)%")

def parse_input():
  nodes = []
  for line in fileinput.input():
    match = PATTERN.match(line)
    if match:
      nodes.append(tuple(map(int,match.groups())))
  return nodes

def part1(nodes):
  viable = []
  for A,B in permutations(nodes,2):
    x,y,size,used,_,percentage = A
    x,y,size,_,avail,percentage = B
    if used and used <= avail:
      viable.append((A,B))
  return len(viable)

def part2(nodes):
  data = { node[:2]: node[2:] for node in nodes }
  map = dict()
  for coord in data:
    if data[coord][1] > 400:
      map[coord] = "#"
    elif data[coord][1] > 0:
      map[coord] = "."
    else:
      print(coord)
      map[coord] = "_"
  dimx = max(map, key=lambda x:x[0])[0]+1
  dimy = max(map, key=lambda x:x[1])[1]+1
  print(dimx,dimy)
  for y in range(dimy):
    print("".join(map[(x,y)] for x in range(dimx)))

def main():
  nodes = parse_input()
  #print(part1(nodes))
  print(part2(nodes))

if __name__ == "__main__":
  main()
