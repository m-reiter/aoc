#!/usr/bin/python3

import fileinput

def part2(program):
  image = []
  x = 1
  for line in range(6):
    row = []
    for column in range(40):
      row.append("#" if abs(column-x)<2 else ".")
      x = x+program[1+40*line+column]
    image.append("".join(row))
  return image

def main():
  program = [1]
  for line in fileinput.input():
    program.append(0)
    if line.startswith("add"):
      program.append(int(line.split()[1]))

  results = [step*sum(program[:step]) for step in range(20,221,40)]

  print(sum(results))

  for line in part2(program):
    print(line)

if __name__ == "__main__":
  main()
