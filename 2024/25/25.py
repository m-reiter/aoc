#!/usr/bin/python3

import fileinput
from more_itertools import split_at

FULL = "#"

def is_blank(line):
  return not(line.strip())

class LockOrKey:
  @classmethod
  def from_schematic(cls, schematic):
    if schematic[0][0] == FULL:
      return Lock(schematic)
    else:
      return Key(schematic)

  def __init__(self, schematic):
    self.columns = [ 0 ] * 5

    for line in schematic[1:-1]:
      for x, occupied in enumerate(line.strip()):
        self.columns[x] += occupied == FULL

  def __repr__(self):
    return f"<{self.__class__.__name__}: ({','.join(map(str, self.columns))})>"

  def fits(self, other):
    if type(self) == type(other):
      return False
    return all(s + o <= 5 for s, o in zip(self.columns, other.columns))

class Lock(LockOrKey):
  pass

class Key(LockOrKey):
  pass

def get_input():
  items = [ LockOrKey.from_schematic(schematic) for schematic in split_at(fileinput.input(), is_blank) ]
  locks = [ item for item in items if type(item) == Lock ]
  keys = [ item for item in items if type(item) == Key ]
  return locks, keys

def main():
  locks, keys = get_input()

  # part 1
  print(sum(sum(lock.fits(key) for key in keys) for lock in locks))

if __name__ == "__main__":
  main()
