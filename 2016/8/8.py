#!/usr/bin/python3

import fileinput
import re
from collections import deque

GETVALUES = re.compile("(\d+)(?:x| by )(\d+)")

class Display:
  def __init__(self,width,height):
    self.rows = [ deque("."*width) for _ in range(height) ]

  def __repr__(self):
    return "\n".join("".join(row) for row in self.rows)

  def rect(self,width,height):
    for x in range(width):
      for y in range(height):
        self.rows[y][x] = "#"

  def rotate_row(self,row,amount):
    self.rows[row].rotate(amount)

  def rotate_column(self,column,amount):
    aux = deque(row[column] for row in self.rows)
    aux.rotate(amount)
    for row,value in zip(self.rows,aux):
      row[column] = value

  def get_lit_number(self):
    return sum(row.count("#") for row in self.rows)

def parse_input():
  commands = []
  for line in fileinput.input():
    if line.startswith("rect"):
      command = Display.rect
    elif line.startswith("rotate column"):
      command = Display.rotate_column
    elif line.startswith("rotate row"):
      command = Display.rotate_row
    else:
      raise ValueError
    coords = GETVALUES.search(line).groups()
    commands.append((command,)+tuple(map(int,coords)))
  return commands

def part1(commands,width=50,height=6):
  display = Display(width,height)
  for instruction,first,second in commands:
    #print(instruction,first,second)
    instruction(display,first,second)
    print(display,"\n")
  return display.get_lit_number()

def main():
  commands = parse_input()
  print(part1(commands))

if __name__ == "__main__":
  main()
