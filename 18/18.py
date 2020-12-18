#!/usr/bin/python3

import fileinput
import re

REMATCHTYPE = type(re.match("",""))

def calculate(expression, precedence = [r"+*"]):

  if isinstance(expression, REMATCHTYPE):
    expression = expression.group(1)

  operands = re.findall(r"\d+", expression)
  operators = re.findall(r"[+*]", expression)

  for current_operators in precedence:

    new_operands = [operands.pop(0)]
    new_operators = []
    
    for operand,operator in zip(operands,operators):
    
      if operator in current_operators:
      
        new_operands.append(str(eval(new_operands.pop()+operator+operand)))

      else:

        new_operands.append(operand)
        new_operators.append(operator)

    operands = new_operands
    operators = new_operators

  return(operands[0])

def reduce(expression, precedence = [r"+*"]):

  while "(" in expression:
    expression = re.sub(r"\(([^()]+)\)", lambda x: calculate(x, precedence), expression)

  return expression

def evaluate(expression, precedence = [r"+*"]):

  return int(calculate(reduce(expression, precedence), precedence))

def main():
  
  input_ = list(fileinput.input())

  # part 1

  print(sum(evaluate(line) for line in input_))

  # part 2

  print(sum(evaluate(line, precedence = [r"+", r"*"]) for line in input_))

if __name__ == "__main__":
  main()
