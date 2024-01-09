#!/usr/bin/python3

import fileinput

def read_input():
  programs = set()
  supported = set()
  raw_weights = {}
  full_weights = {}
  supporting = {}
  
  for program in fileinput.input():
    program = program.strip()
    is_supporter = False
    if " -> " in program:
      is_supporter = True
      program, holds = program.split(" -> ")
      for held in holds.split(", "):
        supported.add(held)
    program,weight = program.split()
    weight = int(weight.strip("()"))
    programs.add(program)
    raw_weights[program] = weight
    if is_supporter:
      supporting[program] = holds.split(", ")
    else:
      full_weights[program] = weight

  return programs,supported,raw_weights,full_weights,supporting

def main():
  programs,supported,raw_weights,full_weights,supporting = read_input()
  print((programs-supported).pop())

  #part 2
  checked = set()
  while True:
    to_check = [(program,supported) for program,supported in supporting.items() if all(p in full_weights.keys() for p in supported) and program not in checked]
    for program,supported in to_check:
      weights = [full_weights[p] for p in supported]
      if len(set(weights)) == 1:
        full_weights[program] = raw_weights[program] + sum(weights)
        checked.add(program)
      else:
        print(program,supported,weights)
        for p in supported:
          print(p, raw_weights[p])
        return

if __name__ == "__main__":
  main()
