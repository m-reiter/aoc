#!/usr/bin/python3

import fileinput
from functools import reduce
from operator import add, mul
from collections import defaultdict

OPERATORS = {
  '+': add,
  '*': mul
}

def calculate(operator, terms, verbose = True):
  result = reduce(OPERATORS[operator], map(int, terms))
  if verbose:
    print(f" {operator} ".join(term for term in terms), f"= {result}")
  return result

def main():
  worksheet = {}
  columns = defaultdict(list)
  for line_no, line in enumerate(fileinput.input()):
    for problem, term in enumerate(line.strip().split()):
      worksheet[(problem, line_no)] = term
    for column, digit in enumerate(line.rstrip()):
      columns[column].append(digit)
  operators = line.strip().split()
  columns = [ () ] + [ columns[i] for i in range(len(columns)) ]

  number_of_problems = problem + 1
  number_of_terms = line_no + 1

  verbose = number_of_problems <= 10

  # part 1
  total_sum = 0
  for problem in range(number_of_problems):
    *terms, operator = [ worksheet[(problem, line_no)] for line_no in range(number_of_terms) ]
    total_sum += calculate(operator, terms, verbose)

  print(total_sum)

  # part 2
  total_sum = 0
  problem = number_of_problems - 1 # not necessary since still set from reading input, added for robustness
  while problem >= 0:
    operator = operators[problem]
    terms = []
    while digits := [ character for character in columns.pop() if character.isdigit() ]:
      terms.append("".join(digits))
    problem -= 1
    total_sum += calculate(operator, terms, verbose)
    
  print(total_sum)

if __name__ == "__main__":
  main()
