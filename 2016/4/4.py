#!/usr/bin/python3

import fileinput
import re
from collections import Counter
from string import ascii_lowercase

PATTERN = re.compile("([a-z|-]*)-(\d*)\[(.*)\]")
CODETABLE = ascii_lowercase

def read_data():
  return [ PATTERN.match(line).groups() for line in fileinput.input() ]

def validate(name,checksum):
  occurences = Counter(name)
  del occurences["-"]
  return checksum == "".join(sorted(occurences.keys(), key = lambda x: (-occurences[x],x))[:5])

def decode(name,sector):
  return "".join(" " if letter == "-" else CODETABLE[(CODETABLE.index(letter)+sector)%len(CODETABLE)] for letter in name)

def main():
  data = read_data()
  data = [ (name,int(sector)) for name,sector,checksum in data if validate(name,checksum) ]
  part1 = sum(x[1] for x in data)
  print(part1)
  for name,sector in data:
    if decode(name,sector) == "northpole object storage":
      print(sector)
      break

if __name__ == "__main__":
  main()
