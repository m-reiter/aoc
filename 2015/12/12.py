#!/usr/bin/python3

import fileinput
import re

NUMBER = re.compile("-?\d+")
OBJECT = re.compile("{[^{}]+}")

def calc_sum(text):
  return sum(map(int,NUMBER.findall(text)))

def main():
  my_input = fileinput.input().readline().strip()

  # part 1
  print(calc_sum(my_input))

  # part 2
  while True:
    objects = OBJECT.findall(my_input)
    if not objects:
      break

    for o in objects:
      if "red" in eval(o).values():
        replacement = 0
      else:
        replacement = calc_sum(o)

    my_input = my_input.replace(o,"[{}]".format(replacement))

  print(calc_sum(my_input))

if __name__ == "__main__":
  main()
