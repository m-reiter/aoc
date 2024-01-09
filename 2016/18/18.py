#!/usr/bin/python3

import fileinput

TRAPS = [ '^^.', '.^^', '^..', '..^' ]
TRAP = '^'
SAFE= '.'

def new_row(row):
  aux = SAFE+row+SAFE
  return "".join(TRAP if aux[i:i+3] in TRAPS else SAFE for i in range(len(row)))

def part1(start,rows=40):
  maze = [ start ]
  while len(maze) < rows:
    maze.append(new_row(maze[-1]))
#  print("\n".join(maze))
  return sum(line.count(SAFE) for line in maze)

def main():
  start = fileinput.input().readline().strip()
  print(part1(start))
  print(part1(start,rows=400000))

if __name__ == "__main__":
  main()
