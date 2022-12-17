#!/usr/bin/python3

import fileinput

def read_input():
  days_left = list(map(int,fileinput.input().readline().split(",")))
  fish = [ days_left.count(i) for i in range(9) ]
  return fish

def next_gen(state):
  new_fish = state[1:]
  new_fish.append(state[0])
  new_fish[6] += state[0]
  return new_fish

def multiply(state,ndays):
  for _ in range(ndays):
    state = next_gen(state)
  return state

def part1(state):
  return sum(multiply(state,80))

def part2(state):
  return sum(multiply(state,256))

def main():
  initial_state = read_input()
  print(part1(initial_state))
  print(part2(initial_state))

if __name__ == "__main__":
  main()
