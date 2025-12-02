#!/usr/bin/python3

import fileinput

DIRECTIONS = {
  'L': -1,
  'R':  1
}

def main():
  rotations = [ (DIRECTIONS[line[0]], int(line[1:])) for line in fileinput.input() ]

  # part 1
  position = 50

  print(sum( (position := (position + sign * amount) % 100) == 0 for sign, amount in rotations))

  # part 2
  position = 50
  clicks = 0

  for sign, amount in rotations:
    full_turns, remainder = divmod(amount, 100)
    clicks += full_turns

    start = position
    position += sign * remainder
    if (position <= 0 and start !=0) or position >= 100:
      clicks += 1
    position = position % 100

  print(clicks)

if __name__ == "__main__":
  main()
