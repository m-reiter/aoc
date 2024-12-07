#!/usr/bin/python3

import fileinput
from itertools import product

def add(a, b):
  return a + b

def multiply(a, b):
  return a * b

def parse_line(line):
  result, operands = line.split(":")

  result = int(result)
  operands = tuple(map(int, operands.strip().split()))

  return result, operands

def get_input():
  return [parse_line(line) for line in fileinput.input()]

def validate(equation):
  result, operands = equation
  calculations = product((add, multiply), repeat = len(operands) - 1)
  correct = 0

  for calculation in calculations:
    calculated = operands[0]
    for operator, operand in zip(calculation, operands[1:]):
      calculated = operator(calculated, operand)
    if calculated == result:
      correct += 1

  return correct

def main():
  equations = get_input()

  # part 1
  print(sum(equation[0] for equation in equations if validate(equation)))

if __name__ == "__main__":
  main()
