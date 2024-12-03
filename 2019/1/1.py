#!/usr/bin/python3

import fileinput

def simple_fuel_requirement(mass):
  return int(mass / 3) - 2

def real_fuel_requirement(mass):
  fuel = 0

  while True:
    mass = simple_fuel_requirement(mass)
    if mass <= 0:
      break
    fuel += mass

  return fuel

def main():
  modules = list(map(int, fileinput.input()))

  # part 1
  print(sum(map(simple_fuel_requirement, modules)))

  # part 2
  print(sum(map(real_fuel_requirement, modules)))

if __name__ == "__main__":
  main()
