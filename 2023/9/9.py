#!/usr/bin/python3

import fileinput

from more_itertools import pairwise

def next(history):
  stack = [ history ]
  while True:
    differences = [ b - a for a, b in pairwise(stack[-1]) ]
    if all(d == 0 for d in differences):
      break
    stack.append(differences)
  while len(stack) > 1:
    d = stack.pop().pop()
    stack[-1].append(stack[-1][-1] + d)
  return stack.pop().pop()

def main():
  histories = [ list(map(int, line.split())) for line in fileinput.input() ]

  # part 1
  print(sum(next(h) for h in histories))

  # part 2
  print(sum(next(list(h[::-1])) for h in histories))

if __name__ == "__main__":
  main()
