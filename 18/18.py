#!/usr/bin/python3

import fileinput
import re

REMATCHTYPE = type(re.match("",""))

def calculate(expression, precedence = ["+*"]):

  if isinstance(expression, REMATCHTYPE):
    expression = expression.group(1)

  operands = re.findall(r"\d+", expression)
  operators = re.findall(r"[+*]", expression)

  result = operands.pop(0)

  for operator,operand in zip(operators,operands):

    result = eval(str(result)+operator+operand)

  return(str(result))

def reduce(expression):

  while "(" in expression:
    expression = re.sub(r"\(([^()]+)\)", calculate, expression)

  return expression

def evaluate(expression):

  return int(calculate(reduce(expression)))

def main():
  
  input_ = list(fileinput.input())

  # part 1

  print(sum(evaluate(line) for line in input_))

if __name__ == "__main__":
  main()
