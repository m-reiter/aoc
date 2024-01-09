#!/usr/bin/python3

import fileinput
import re

from more_itertools import chunked
from collections import deque

MAP_HEADER = re.compile("(\w+)-to-(\w+) map:")

class Collection(deque):
  """
  represents a collection of items

  contents are tuples, each tuple presents an interval of item numbers by its first and last elements

  Attributes
  ----------
  kind : category of items this represents

  Methods
  -------
  normalize : sort and consolidate any overlapping intervals
  """

  def __init__(self, kind, *args, from_integers = None, from_intervals = None, **kwargs):
    super().__init__(*args, **kwargs)
    self.kind = kind
    if from_integers:
      self.extend((i, i) for i in from_integers)
    elif from_intervals:
      self.extend((start, start + length - 1) for start, length in chunked(from_intervals, 2))
    self.normalize()

  def __repr__(self):
    return "Collection of {}s, {} intervals: {}".format(self.kind, len(self), tuple(self))

  def normalize(self):
    original = deque(sorted(self))
    self.clear()

    while original:
      start, end = original.popleft()
      while original and end >= original[0][0]:
        end = max(end, original.popleft()[1])
      self.append((start, end))


class MappingRange:
  def __init__(self, line):
    (
      target,
      self.start,
      length
    ) = map(int, line.split())
    self.end = self.start + length - 1
    self.offset = target - self.start

  def __repr__(self):
    return "MappingRange: {}-{} -> {}-{}".format(
      self.start,
      self.end,
      self.start + self.offset,
      self.end + self.offset
    )

  def __contains__(self, other):
    return self.start <= other[1] and self.end >= other[0]

  def __getitem__(self, collection):
    unhandled = Collection(collection.kind)
    processed = []
    
    for interval in collection:
      if interval in self:
        start, end = interval
        if start < self.start:
          unhandled.append((start, self.start - 1))
          start = self.start
        if end > self.end:
          unhandled.append((self.end + 1, end))
          end = self.end
        processed.append((start + self.offset, end + self.offset))
      else:
        unhandled.append(interval)

    return unhandled, processed


class Mapping:
  def __init__(self, source, target):
    self.source = source
    self.target = target
    self.ranges = []

  def __add__(self, other):
    if isinstance(other, MappingRange):
      self.ranges.append(other)
      return self
    raise ValueError

  def __getitem__(self, collection):
    result = Collection(self.target)
    unhandled = collection

    for r in self.ranges:
      unhandled, processed = r[unhandled]
      result.extend(processed)

    result.extend(unhandled)
    result.normalize()

    return result


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

    return self[collection.kind][collection] 


class State:
  def __init__(self, seeds, ruleset):
    self.ruleset = ruleset
    self.collections = [ seeds ]

  def evolve(self):
    while self.collections[-1].kind in self.ruleset:
      self.collections.append(self.ruleset.process(self.collections[-1]))


def read_state():
  ruleset = Ruleset()

  seeds, *mappings = "".join(fileinput.input()).strip().split("\n\n")

  seeds = list(map(int, seeds.split(": ")[1].split()))

  for m in mappings:
    header, *ranges = m.split("\n")

    source, target = MAP_HEADER.match(header).groups()
    
    mapping = Mapping(source, target)

    for r in ranges:
      mapping += MappingRange(r)

    ruleset += mapping

  return seeds, ruleset


def main():
  seeds, ruleset = read_state()

  # part 1
  state = State(Collection("seed", from_integers = seeds), ruleset)
  state.evolve()

  print(min(state.collections[-1])[0])

  # part 2
  state = State(Collection("seed", from_intervals = seeds), ruleset)
  state.evolve()

  print(min(state.collections[-1])[0])

if __name__ == "__main__":
  main()
