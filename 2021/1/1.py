#!/usr/bin/python3

import fileinput
from more_itertools import pairwise,windowed

def count_increases(iterable):
  return sum(y > x for x,y in pairwise(iterable))

def main():
  data = list(map(int,fileinput.input()))
  solution_1 = count_increases(data)
  print(solution_1)
  solution_2 = count_increases(map(sum,windowed(data,3)))
  #solution_2 = list(windowed(data,3))
  print(solution_2)

if __name__ == "__main__":
  main()
