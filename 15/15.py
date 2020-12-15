#!/usr/bin/python3

STARTING_NUMBERS = [18,8,0,5,4,1,20]

from collections import defaultdict

class MemoryGame:

  def __init__(self, starting_numbers):

    self.starting_numbers = starting_numbers

    self.reset()

  def reset(self):

    self.turn = 1
    self.last_number = None
    self.seen = defaultdict(list)

  def step(self, verbose = True):

    if self.turn <= len(self.starting_numbers):

      number = self.starting_numbers[self.turn-1]

    else:

      seen = self.seen[self.last_number]
      
      if len(seen) == 1:
      
        number = 0

      else:

        number = seen[-1] - seen[-2]

    self.seen[number].append(self.turn)
    self.last_number = number

    if verbose:
      print("{:4d}: {:4d}".format(self.turn, number))

    self.turn += 1

  def run(self, exit_condition = bool, verbose = True):

    while not exit_condition():

      self.step(verbose)

def main():
  
  game = MemoryGame(STARTING_NUMBERS)

  game.run(lambda: game.turn > 2020)
  
  solution_part1 = game.last_number

  game.run(lambda: game.turn > 30000000, verbose = False)
  
  solution_part2 = game.last_number

  print("part 1: {}".format(solution_part1))
  print("part 2: {}".format(solution_part2))

if __name__ == "__main__":
  main()
