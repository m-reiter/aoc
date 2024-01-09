#!/usr/bin/python3

from math import floor, sqrt

INPUT = 36000000

def presents(house):
  divisors = { x for x in range(1, floor(sqrt(house)) + 1) if house % x == 0 }
  additional_divisors = { house // x for x in divisors }
  divisors |= additional_divisors
  return 10 * sum(divisors), 11 * sum(x for x in divisors if house // x <= 50)

def main():
  houses = []
  house = 1
  part1 = 0
  part2 = 0
  while True:
    a, b = presents(house)
    if a > INPUT and not part1:
      part1 = house
    if b > INPUT and not part2:
      part2 = house
    if part1 and part2:
      break
    #if house % 10000 == 0:
    #  print(house, houses[-1])
    house += 1
  print(part1)
  print(part2)

if __name__ == "__main__":
  main()
