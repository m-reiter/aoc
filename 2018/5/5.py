#!/usr/bin/python3

import fileinput
import string
import re

TRIGGERS = re.compile("|".join("".join(x) for x in zip(string.ascii_lowercase+string.ascii_uppercase,string.ascii_uppercase+string.ascii_lowercase)))

def react(polymer):
  while TRIGGERS.search(polymer):
    polymer = TRIGGERS.sub("",polymer)

  return polymer

def main():
  polymer = fileinput.input().readline().strip()

  #part 1
  print(len(react(polymer)))

  #part 2
  units = set(polymer.lower())
  results = { unit: len(react(re.sub("(?i){}".format(unit),"",polymer))) for unit in units }

  print(min(results.values()))

if __name__ == "__main__":
  main()
