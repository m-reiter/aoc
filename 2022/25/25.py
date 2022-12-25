#!/usr/bin/python3

import fileinput
from numpy import base_repr

VALUES = {
  "=": -2,
  "-": -1,
  "0": 0,
  "1": 1,
  "2": 2
}
SYMBOLS = { str(number + 2): symbol for symbol, number in VALUES.items() }

def desnafu(number):
  return sum(VALUES[char] * 5**n for n,char in enumerate(reversed(number)))

def snafu(number):
  digits = 1
  limit = 2
  while not -limit <= number <= limit:
    limit += 2 * 5**digits
    digits += 1
  return "".join(SYMBOLS[char] for char in base_repr(number + limit,5))

def main():
  requirements = [line.strip() for line in fileinput.input()]

  print(snafu(sum(desnafu(r) for r in requirements)))

if __name__ == "__main__":
  main()
