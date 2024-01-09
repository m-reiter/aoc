#!/usr/bin/python3

import fileinput
import re

from collections import deque

PLANT = "#"
EMPTY = "."

INITIAL_STATE = re.compile("initial state: ([.#]*)")

def get_surroundings(state,index):
  return "".join(PLANT if i in state else EMPTY for i in range(index-2,index+3))

def main():
  with fileinput.input() as puzzle_input:
    pattern = INITIAL_STATE.match(puzzle_input.readline()).groups()[0]
    state = { i for i,pot in enumerate(pattern) if pot == PLANT }

    puzzle_input.readline()

    #growth = { pattern for line in puzzle_input for pattern,result in line.strip().split(" => ") if result == PLANT }
    growth = set()
    for line in puzzle_input:
      pattern,result = line.strip().split(" => ")
      if result == PLANT:
        growth.add(pattern)

    last = 0
    generation = 0
    differences = deque(maxlen = 10)

    while True:
      state = { i for i in range(min(state)-2,max(state)+3) if get_surroundings(state,i) in growth }
      generation += 1

      current = sum(state)

      # part 1
      if generation == 20:
        print(current)

      differences.append(current - last)
      if len(differences) == 10 and len(set(differences)) == 1:
        break

      last = current

    print(current + (50000000000 - generation)*differences.pop())

if __name__ == "__main__":
  main()
