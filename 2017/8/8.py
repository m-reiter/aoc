#!/usr/bin/python3

import fileinput
from collections import defaultdict

def main():
  registers = defaultdict(int)
  all_time_max = 0
  for line in fileinput.input():
    instruction, condition = line.strip().split(" if ")
    register, _, comparison = condition.partition(" ")
    if eval("{} {}".format(registers[register],comparison)):
      register, instruction, value = instruction.split()
      registers[register] += int(value) * (1 if instruction == "inc" else -1)
      all_time_max = max(all_time_max,registers[register])
  print(max(registers.values()))
  print(all_time_max)

if __name__ == "__main__":
  main()
