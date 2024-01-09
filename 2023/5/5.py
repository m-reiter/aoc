#!/usr/bin/python3

import fileinput
import re

from more_itertools import chunked

MAP_HEADER = re.compile("(\w+)-to-(\w+) map:")

class Collection(list):
  def __init__(self, kind, *args, **kwargs):
    super().__init__(*args, **kwargs)
    self.kind = kind

  def __repr__(self):
    return "Collection of {}s: {}".format(self.kind, super().__repr__())

class Range:
  def __init__(self, line):
    (
      self.target,
      self.source,
      self.length
    ) = map(int, line.split())

  def __repr__(self):
    return "Range: {}-{} -> {}-{}".format(
      self.source,
      self.source + self.length - 1,
      self.target,
      self.target + self.length - 1
    )

  def __contains__(self, other):
    try:
      return self.source <= int(other) < self.source + self.length
    except ValueError:
      return False

  def __getitem__(self, key):
    if key in self:
      return self.target + key - self.source
    raise IndexError

class Mapping:
  def __init__(self, source, target):
    self.source = source
    self.target = target
    self.ranges = []

  def __add__(self, other):
    if isinstance(other, Range):
      self.ranges.append(other)
      return self
    raise ValueError

  def __getitem__(self, key):
    for r in self.ranges:
      try:
        return r[key]
      except IndexError:
        pass
    return key

class Ruleset:
  def __init__(self):
    self.mappings = []

  def __getitem__(self, key):
    for mapping in self.mappings:
      if mapping.source == key:
        return mapping
    raise IndexError

  def __contains__(self, other):
    return any(mapping.source == other for mapping in self.mappings)

  def __add__(self, other):
    if isinstance(other, Mapping):
      self.mappings.append(other)
      return self
    raise ValueError

  def process(self, collection):
    assert collection.kind in self

    m = self[collection.kind]
    return Collection(m.target, (m[item] for item in collection))

class State:
  def __init__(self, seeds, ruleset):
    self.ruleset = ruleset
    self.collections = [ seeds ]

  def __add__(self, other):
    if isinstance(other, Collection):
      self.collections.append(other)
      return self
    raise ValueError

  def evolve(self):
    while self.collections[-1].kind in self.ruleset:
      self.collections.append(self.ruleset.process(self.collections[-1]))

def read_state():
  ruleset = Ruleset()

  seeds, *mappings = "".join(fileinput.input()).strip().split("\n\n")

  seeds = Collection("seed", map(int, seeds.split(": ")[1].split()))

  for m in mappings:
    header, *ranges = m.split("\n")

    source, target = MAP_HEADER.match(header).groups()
    
    mapping = Mapping(source, target)

    for r in ranges:
      mapping += Range(r)

    ruleset += mapping

  return State(seeds, ruleset)

def main():
  state = read_state()

  state.evolve()

  # part 1
  print(min(state.collections[-1]))

  # part 2
  seeds = state.collections[0]

  new_seeds = Collection("seed", sum([ list(range(start, start + length)) for start, length in chunked(seeds, 2) ],[]))

  print(len(new_seeds))
  state.collections = [ new_seeds ]

  state.evolve()

  print(min(state.collections[-1]))

if __name__ == "__main__":
  main()
