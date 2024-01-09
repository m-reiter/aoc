#!/usr/bin/python3

import fileinput
import math

from functools import reduce
from operator import mul

def number_of_ways(T, r):
  """
  t : time button is pressed
  T : length of race
  r : current record

  traveled distance is 

  d = (T - t) * t

  solving d = r for t yields

  t**2 -Tt + r = 0

  hence

  t = T/2 +/- sqrt(T**2/4 -r)
  """
  root_term = math.sqrt(T**2 / 4 - r)

  # we need to beat the record, not just achieve it, hence the +/- 1
  min_time_to_beat = math.floor(T / 2 - root_term) + 1
  max_time_to_beat = math.ceil(T / 2 + root_term) - 1

  return max_time_to_beat - min_time_to_beat + 1

def main():
  
  times, records = (list(map(int, line.split()[1:])) for line in fileinput.input())

  # part 1
  possibilities = [ number_of_ways(T, r) for T, r in zip(times, records) ]

  print(reduce(mul, possibilities))

  # part 2
  T = int("".join(str(t) for t in times))
  r = int("".join(str(d) for d in records))

  print(number_of_ways(T, r))

if __name__ == "__main__":
  main()
