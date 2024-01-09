#!/usr/bin/python3

import fileinput

class Card:
  def __init__(self, line):
    card, numbers = line.strip().split(":")
    self.winning, self.guesses = (part.strip().split() for part in numbers.split("|"))
    assert len(set(self.guesses)) == len(self.guesses)
    self.wins = set(self.winning) & set(self.guesses)
    self.value = 2 ** (len(self.wins) - 1) if self.wins else 0

  def __radd__(self, other):
    return other + self.value

def main():
  cards = [ Card(line) for line in fileinput.input() ]

  # part 1
  print(sum(cards))

  # part 2
  card_numbers = [ 1 ] * len(cards)

  for number, card in enumerate(cards):
    for i in range(len(card.wins)):
      card_numbers[number + i + 1] += card_numbers[number]

  print(sum(card_numbers))

if __name__ == "__main__":
  main()
