#!/usr/bin/python3

import fileinput
import operator

MASK = (1 << 16) - 1

FUNCTIONS = {
  "AND":    operator.__and__,
  "OR":     operator.__or__,
  "LSHIFT": operator.__lshift__,
  "RSHIFT": operator.__rshift__,
  "UNITY":  lambda x: x,
  "NOT":    lambda x: ~x
}

def read_input():
  state = {}
  rules = {}

  for line in fileinput.input():
    source, target = line.strip().split(" -> ")
    if source.isnumeric():
      state[target] = int(source)
    else:
      if source.islower():
        prereqs = args = [source]
        operator = "UNITY"
      elif source.startswith("NOT"):
        _, arg = source.split()
        prereqs = args = [arg]
        operator = "NOT"
      else:
        arg1, operator, arg2 = source.split()
        args = [arg1, arg2]
        prereqs = [arg for arg in args if not arg.isnumeric()]
      rules[target] = (prereqs,args,operator)

  return state, rules

def resolve(initial, rules):
  state = initial.copy()

  wanted = list(rules.keys())

  while wanted:
    for target in wanted:
      prereqs, args, func = rules[target]
      if all(arg in state for arg in prereqs):
        args = [int(arg) if arg.isnumeric() else state[arg] for arg in args]
        state[target] = FUNCTIONS[func](*args) & MASK
        wanted.remove(target)

  return state

def main():
  initial, rules = read_input()

  state = resolve(initial,rules)

  if "a" in state:
    print(state["a"])

  initial["b"] = state["a"]

  state = resolve(initial,rules)

  for wire in sorted(state.keys()):
    print("{}: {}".format(wire,state[wire]))
  if "a" in state:
    print(state["a"])


if __name__ == "__main__":
  main()
