#!/usr/bin/python3

import fileinput

def cost(positions,target):
  return sum(abs(x-target) for x in positions)

def real_cost(positions,target):
  return sum(abs(x-target) * (abs(x-target)+1) // 2 for x in positions)

def solve(positions,cost_function):
  costs = [ cost_function(positions,target) for target in range(max(positions)+1) ]
  print(list(enumerate(costs)))
  cheapest = costs.index(min(costs))
  return cheapest,costs[cheapest]

def part1(positions):
  return solve(positions,cost)

def part2(positions):
  return solve(positions,real_cost)

def main():
  positions = list(map(int,fileinput.input().readline().split(",")))
  print(part1(positions))
  print(part2(positions))

if __name__ == "__main__":
  main()
