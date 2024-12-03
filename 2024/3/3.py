#!/usr/bin/python3

import fileinput
import re

MUL = re.compile("mul\(([1-9]\d{0,2}),([1-9]\d{0,2})\)")

def calculate(fragment):
  result = 0
  for mul in MUL.findall(fragment):
    a,b = map(int,mul)
    result += a*b
  return result

def main():
  memory = "".join([line.strip() for line in fileinput.input()])

  # part 1
  print(calculate(memory))

  # part 2
  # correct for conditionals, initial state is enabled
  memory = "".join("".join(fragment.split("do()")[1:]) for fragment in ("do()"+memory).split("don't()"))
  print(calculate(memory))

if __name__ == "__main__":
  main()
