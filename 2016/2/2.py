#!/usr/bin/python3

import fileinput
from P import P

STEPS = {
  'U': P(0,1),
  'D': P(0,-1),
  'L': P(-1,0),
  'R': P(1,0)
}
FIELDS_PART1 = {
  P(0,2): "1", 
  P(1,2): "2",
  P(2,2): "3",
  P(0,1): "4",
  P(1,1): "5",
  P(2,1): "6",
  P(0,0): "7",
  P(1,0): "8",
  P(2,0): "9"
}
FIELDS_PART2 = {
  P(2,4): "1",
  P(1,3): "2",
  P(2,3): "3",
  P(3,3): "4",
  P(0,2): "5",
  P(1,2): "6",
  P(2,2): "7",
  P(3,2): "8",
  P(4,2): "9",
  P(1,1): "A",
  P(2,1): "B",
  P(3,1): "C",
  P(2,0): "D"
}

def move(line,fields=FIELDS_PART1,start=None):
  position = start if start else next(field for field,label in fields.items() if label == "5")
  for instruction in line:
    new = position + STEPS[instruction]
    if new in fields:
      position = new
  return position

def part(instructions,fields=FIELDS_PART1):
  code = ""
  position = None
  for line in instructions:
    position = move(line,fields=fields,start=position)
    code += fields[position]
  print(code)

def main():
  instructions = [line.strip() for line in fileinput.input()]
  part(instructions)
  part(instructions,FIELDS_PART2)

if __name__ == "__main__":
  main()
