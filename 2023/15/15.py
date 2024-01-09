#!/usr/bin/python3

import fileinput
import re

INSTRUCTION = re.compile("([a-z]+)([-=])(\d*)")

def HASH(string):
  _hash = 0

  for char in string:
    _hash = (_hash + ord(char)) * 17 % 256

  return _hash

class Box:
  def __init__(self, number):
    self.number = number
    self.labels = []
    self.lenses = []

  def __str__(self):
    return "Box {:3}: {}".format(self.number, " ".join("[{} {}]".format(label, lens) for label, lens in zip(self.labels, self.lenses)))

  def remove_lens(self, label):
    # returns True if Box is empty after removal
    try:
      index = self.labels.index(label)
      self.labels.pop(index)
      self.lenses.pop(index)
    except ValueError:
      pass

    return not self.labels

  def add_lens(self, label, focal_length):
    try:
      index = self.labels.index(label)
      self.lenses[index] = focal_length
    except ValueError:
      self.labels.append(label)
      self.lenses.append(focal_length)

  def focusing_power(self):
    return (self.number + 1) * sum(position * focal_length for position, focal_length in enumerate(self.lenses, 1))

class Boxes(dict):
  def __getitem__(self, key):
    if not key in self:
      self[key] = Box(key)
    return super().__getitem__(key)
    
def part2(instructions, verbose = True):
  boxes = Boxes()

  for instruction in instructions:
    label, command, value = INSTRUCTION.match(instruction).groups()
    
    box = HASH(label)

    if command == "-":
      if boxes[box].remove_lens(label):
        boxes.pop(box)
    else:
      boxes[box].add_lens(label, int(value))

    if verbose:
      print('After "{}":'.format(instruction))
      for number, box in sorted(boxes.items())[:10]:
        print(box)
      if len(boxes) > 10:
        print("[...] ({} box{} omitted)".format(len(boxes) - 10, "es" if len(boxes) > 11 else ""))
      print()

  return sum(map(Box.focusing_power, boxes.values()))

def main():
  instructions = list(fileinput.input().readline().strip().split(","))

  # part 1
  print(sum(map(HASH, instructions)))

  # part 2
  verbose = len(instructions) < 20
  print(part2(instructions, verbose))

if __name__ == "__main__":
  main()
