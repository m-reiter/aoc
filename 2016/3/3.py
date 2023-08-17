#!/usr/bin/python3

import fileinput
from more_itertools import chunked,flatten

def is_valid_triangle(sides):
  return sum(sides) - max(sides) > max(sides)

def main():
  triangles = [ tuple(map(int,map(str.strip,line.split()))) for line in fileinput.input() ]
  print("part1:",sum(map(is_valid_triangle,triangles)))
  new_triangles = flatten(zip(*trio) for trio in chunked(triangles,3))
  print("part2:",sum(map(is_valid_triangle,new_triangles)))

if __name__ == "__main__":
  main()
