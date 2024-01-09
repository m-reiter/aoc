#!/usr/bin/python3

import fileinput
import re
import copy
import string
from collections import defaultdict

CONDITION = re.compile("Step (.) must be finished before step (.) can begin.")
WORKERS = 5
BASE_DURATION = 60

def main():
  blockers = defaultdict(set)
  for condition in fileinput.input():
    first,second = CONDITION.match(condition).groups()
    blockers[second].add(first)
    blockers[first]
  number_of_steps = len(blockers)
  save = copy.deepcopy(blockers)

  solution = []
  while len(solution) < number_of_steps:
    candidates = [step for step,condition in blockers.items() if not condition]
    next_step = min(candidates)
    solution.append(next_step)
    del blockers[next_step]
    for condition in blockers.values():
      condition.discard(next_step)

  print("".join(solution))

  # part 2
  blockers = save
  second = 0
  busy = 0
  finished = 0
  in_progress = defaultdict(set)
  while finished < number_of_steps:
    if busy < WORKERS:
      candidates = {step for step,condition in blockers.items() if not condition}
      for _ in range(min(len(candidates),WORKERS-busy)):
        next_step = min(candidates)
        del blockers[next_step]
        candidates.remove(next_step)
        busy += 1
        end_time = second + BASE_DURATION + string.ascii_uppercase.index(next_step) + 1
        in_progress[end_time].add(next_step)
    second += 1
    for step in in_progress[second]:
      for condition in blockers.values():
        condition.discard(step)
      busy -= 1
      finished += 1

  print(second)

if __name__ == "__main__":
  main()
