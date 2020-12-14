#!/usr/bin/python3

MINTIME = 100000000000000
MINTIME = 1

import fileinput
from math import gcd
from collections import defaultdict

def kgv(a, b):

  return a * b // gcd(a, b)

def solve_next_bus(start, step, pos, id):

  i = 0

  while (start +i*step + pos) % id != 0:
    
    i += 1

  new_step = kgv(step, id)

  return start +i*step, new_step, i+1

def main():
  
  # part 1

  input_ = fileinput.input()

  arrival = int(input_.readline())

  buses = { pos: int(id) for pos,id in enumerate(input_.readline().strip().split(",")) if id.isnumeric() }

  departures = { id: id * (arrival // id + (1 if arrival % id else 0)) for id in buses.values() }

  busid, departure = min(departures.items(), key = lambda x: x[1])

  print(busid * (departure - arrival))

  # part 2

  bus_zero = buses.pop(0)
  timestamp = (MINTIME // bus_zero) * bus_zero
  step = bus_zero
  iterations = 0

  for pos, id in buses.items():
    print(timestamp, step)
    timestamp, step, i = solve_next_bus(timestamp, step, pos, id)
    iterations += i

  print(timestamp, iterations)

if __name__ == "__main__":
  main()
