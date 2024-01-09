#!/usr/bin/python3

import fileinput
import re
from collections import deque

SWAP_POSITIONS = re.compile("swap position (\d+) with position (\d+)")
SWAP_LETTERS = re.compile("swap letter (.) with letter (.)")
ROTATE_LR = re.compile("rotate (left|right) (\d+) step")
ROTATE_POS = re.compile("rotate based on position of letter (.)")
REVERSE_XY = re.compile("reverse positions (\d+) through (\d+)")
MOVE_XY = re.compile("move position (\d+) to position (\d+)")

def rotate(string,amount):
  aux = deque(string)
  aux.rotate(amount)
  return "".join(aux)
  
def execute(instruction,string):
  if SWAP_POSITIONS.match(instruction):
    x,y = sorted(map(int,SWAP_POSITIONS.match(instruction).groups()))
    string = string[:x]+string[y]+string[x+1:y]+string[x]+string[y+1:]
  elif SWAP_LETTERS.match(instruction):
    x,y = SWAP_LETTERS.match(instruction).groups()
    trans = str.maketrans(x+y,y+x)
    string = string.translate(trans)
  elif ROTATE_LR.match(instruction):
    direction,amount = ROTATE_LR.match(instruction).groups()
    amount = int(amount)
    if direction == "left":
      amount = -amount
    string = rotate(string,amount)
  elif ROTATE_POS.match(instruction):
    letter = ROTATE_POS.match(instruction).group(1)
    amount = string.index(letter)
    amount += 2 if amount >=4 else 1
    string = rotate(string,amount)
  elif REVERSE_XY.match(instruction):
    x,y = sorted(map(int,REVERSE_XY.match(instruction).groups()))
    string = string[:x]+"".join(reversed(string[x:y+1]))+string[y+1:]
  elif MOVE_XY.match(instruction):
    x,y = map(int,MOVE_XY.match(instruction).groups())
    letter = string[x]
    string = string[:x]+string[x+1:]
    string = string[:y]+letter+string[y:]
  return string

def reverse(instruction,string):
  if ROTATE_LR.match(instruction):
    direction,amount = ROTATE_LR.match(instruction).groups()
    amount = int(amount)
    if direction == "right":
      amount = -amount
    string = rotate(string,amount)
  elif ROTATE_POS.match(instruction):
    letter = ROTATE_POS.match(instruction).group(1)
    amount = 1
    while True:
      rotated = rotate(string,-amount)
      index = rotated.index(letter)
      if amount == index + (2 if index >=4 else 1):
        break
      amount += 1
    string = rotated
  elif MOVE_XY.match(instruction):
    x,y = map(int,MOVE_XY.match(instruction).groups())
    letter = string[y]
    string = string[:y]+string[y+1:]
    string = string[:x]+letter+string[x:]
  else:
    return execute(instruction,string)
  return string

def scramble(string,instructions):
  for instruction in instructions:
    string = execute(instruction,string)
  return string

def unscramble(string,instructions):
  for instruction in reversed(instructions):
    string = reverse(instruction,string)
  return string

def main():
  instructions = [ line.strip() for line in fileinput.input() ]
  print(scramble("abcdefgh",instructions))
  print(unscramble("fbgdceah",instructions))

if __name__ == "__main__":
  main()
