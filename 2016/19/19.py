#!/usr/bin/python3

from collections import deque

ELVES = 5
ELVES = 3017957

def part1():
  elves = deque((i+1,1) for i in range(ELVES))
  while len(elves) > 1:
    elves[0] = (elves[0][0],elves[0][1]+elves[1][1])
    elves.rotate(-1)
    elves.popleft()
  print(elves)

def part2():
  elves = deque(i+1 for i in range(ELVES))
  while len(elves) > 1:
    giver = int(len(elves)/2)
    elves.rotate(-giver)
    elves.popleft()
    elves.rotate(giver-1)
    #print(len(elves))
    #if len(elves) % 10000 == 0: print(len(elves))
  print(elves)

def part2b():
  left = deque(i+1 for i in range(ELVES // 2))
  right = deque(i+1 for i in range(ELVES // 2,ELVES))
  while len(left)+len(right) > 1:
    right.popleft()
    right.append(left.popleft())
    if len(left) < len(right)-1:
      left.append(right.popleft())
    #if len(elves) % 1000 == 0: print(len(elves))
  print(right[0] or left[0])

def main():
  #part1()
  part2b()

if __name__ == "__main__":
  main()
