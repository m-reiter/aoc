#!/usr/bin/python3

import fileinput
from collections import deque

def part(banned,max_ip=9,part1=True):
  allowed = 0
  current = 0
  while current <= max_ip:
    if not banned or current < banned[0][0]:
      if part1:
        return current
      if not banned:
        allowed += max_ip+1-current
        current = max_ip+1
      else:
        allowed += banned[0][0]-current
        current = banned[0][0]
    else:
      current = max(current,banned.popleft()[1]+1)
  return allowed

def main():
  banned = deque(sorted(tuple(map(int,line.split("-"))) for line in fileinput.input()))
  print(part(banned.copy(),max_ip=2**32-1))
  print(part(banned.copy(),max_ip=2**32-1,part1=False))

if __name__ == "__main__":
  main()
