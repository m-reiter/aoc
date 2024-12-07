#!/usr/bin/python3

import fileinput
from itertools import product

def add(a, b):
  return a + b

def multiply(a, b):
  return a * b

def concatenate(a, b):
  return int(str(a) + str(b))

def parse_line(line):
  result, operands = line.split(":")

  result = int(result)
  operands = tuple(map(int, operands.strip().split()))

  return result, operands

def get_input():
  return [parse_line(line) for line in fileinput.input()]

def validate(equation, operations = (add, multiply)):
  result, operands = equation
  calculations = product(operations, repeat = len(operands) - 1)
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

  # part 2
  print(sum(equation[0] for equation in equations if validate(equation, operations = (add, multiply, concatenate))))

if __name__ == "__main__":
  main()
