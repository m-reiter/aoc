#!/usr/bin/python3

import fileinput

from collections import defaultdict
from functools import reduce
from operator import mul

def read_input():
  games = defaultdict(list)

  for line in fileinput.input():
    game, samples = line.strip().split(":")
    game = int(game.split()[1])

    samples = samples.split(";")

    for sample in samples:
      balls = defaultdict(int)
      for color in sample.split(","):
        number, color = color.strip().split()
        balls[color] = int(number)
      games[game].append(balls)

  return games
      
def main():
  games = read_input()

  # part 1
  available = {
    "red":    12,
    "green":  13,
    "blue":   14
  }

  sum_of_IDs = 0

  # part 2
  powers = defaultdict(int)
  
  for ID, game in games.items():
    possible = True
    needed = defaultdict(int)
    for sample in game:
      possible &= all(sample[color] <= available[color] for color in available)
      for color in available:
        needed[color] = max(needed[color],sample[color])
    sum_of_IDs += ID * possible
    powers[ID] = reduce(mul, needed.values())
  
  print(sum_of_IDs)

  print(sum(powers.values()))

if __name__ == "__main__":
  main()
