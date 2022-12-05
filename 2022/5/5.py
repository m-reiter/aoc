#!/usr/bin/python3

import fileinput
import re
from collections import deque
from more_itertools import chunked

MOVE = re.compile("move (\d+) from (\d+) to (\d+)")

def read_stacks(f):
  stacks = []
  for line in f:
    items = [ item[1] for item in chunked(line, 4) ]
    if items[0] != "1":
      if len(stacks) < len(items):
        stacks.extend([ deque() for _ in range(len(items)-len(stacks)) ])
      for stack,item in zip(stacks,items):
        if item != " ":
          stack.appendleft(item)
    else:
      assert len(stacks) == int(line.split()[-1])
      f.readline()
      return stacks

def read_moves(f):
  return [ tuple(map(int,MOVE.match(line).groups())) for line in f ]

def move_crates(stacks,number,origin,destination):
  for _ in range(number):
    stacks[destination-1].append(stacks[origin-1].pop())

def move_crates_9001(stacks,number,origin,destination):
  stacks[destination-1].extend(stacks[origin-1][-number:])
  del stacks[origin-1][-number:]

def part1(stacks,moves):
  stacks = [stack.copy() for stack in stacks]
  for number,origin,destination in moves:
    move_crates(stacks,number,origin,destination)
  return "".join(stack[-1] for stack in stacks)

def part2(stacks,moves):
  stacks = [list(stack) for stack in stacks]
  for number,origin,destination in moves:
    move_crates_9001(stacks,number,origin,destination)
  return "".join(stack[-1] for stack in stacks)

def main():
  with fileinput.input() as f:
    stacks = read_stacks(f)
    moves = read_moves(f)
  print(part1(stacks, moves))
  print(part2(stacks, moves))

if __name__ == "__main__":
  main()
