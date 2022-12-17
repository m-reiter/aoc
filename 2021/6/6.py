#!/usr/bin/python3

import fileinput

def next_gen(state):
  new_fish = [ 8 ] * state.count(0)
  next_gen = [ fish-1 if fish != 0 else 6 for fish in state ] + new_fish
  return next_gen

def multiply(state,ndays):
  for _ in range(ndays):
    print(_, len(state))
    state = next_gen(state)
  return state

def part1(state):
  return len(multiply(state,80))

def part2(state):
  return len(multiply(state,256))

def main():
  initial_state = list(map(int,fileinput.input().readline().split(",")))
  print(part1(initial_state))
  print(part2(initial_state))

if __name__ == "__main__":
  main()
