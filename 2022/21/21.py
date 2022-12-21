#!/usr/bin/python3

import fileinput
from numpy import sign

def read_input():
  yelling = {}
  waiting = []
  for line in fileinput.input():
    monkey,job = line.strip().split(": ")
    first,*rest = job.split()
    if not rest:
      yelling[monkey] = int(first)
    else:
      waiting.append((monkey,rest[0],(first,rest[1])))
  return yelling,waiting

def part1(yelling,waiting):
  yelling = yelling.copy()
  while True:
    remaining = []
    for monkey,operation,args in waiting:
      if all(arg in yelling.keys() for arg in args):
        yelling[monkey] = eval("{} {} {}".format(yelling[args[0]],operation,yelling[args[1]]))
        if monkey == "root":
          return int(yelling[monkey])
      else:
        remaining.append((monkey,operation,args))
    if not remaining:
      raise Exception
    waiting = remaining
        
def part2(yelling,waiting):
  yelling = yelling.copy()
  yelling["humn"] = "humn"
  while True:
    remaining = []
    for monkey,operation,args in waiting:
      if not all(arg in yelling.keys() for arg in args):
        remaining.append((monkey,operation,args))
      else:
        if monkey != "root":
          yelling[monkey] = "({} {} {})".format(yelling[args[0]],operation,yelling[args[1]])
        else:
          for arg in args:
            value = yelling[arg]
            if "humn" in value:
              formula = value
            else:
              target = eval(value)
          humn = 0
          value = eval(formula)
          sgn = sign(target-value)
          humn = 1
          while sign(target-eval(formula)) == sgn:
            humn *= 10
          sgn = -sgn
          step = - humn // 2
          while True:
            humn += step
            value = eval(formula)
            if value == target:
              return humn
            elif sign(target-value) != sgn:
              sgn = -sgn
              step = step // -2
    if not remaining:
      raise Exception
    waiting = remaining
        
def main():
  yelling,waiting = read_input()

  print(part1(yelling,waiting))
  print(part2(yelling,waiting))

if __name__ == "__main__":
  main()
