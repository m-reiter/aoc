#!/usr/bin/python3

import fileinput

from more_itertools import split_at
from attr import attrs, attrib

def is_blank(line):
  return not line.strip()

@attrs
class Card:
  numbers = attrib(factory = dict)
  marks = attrib(factory = list)
  has_won = attrib(default = False)
  winning_number = attrib(default = None)

  @classmethod
  def from_lines(cls, lines):
    card = cls()

    for y, line in enumerate(lines):
      for x, number in enumerate(map(int, line.strip().split())):
        card.numbers[number] = (x, y)

    return card

  def check_win(self):
    return any(all((x, y) in self.marks for x in range(5)) for y in range(5)) or any(all((x,y) in self.marks for y in range(5)) for x in range(5))

  def draw_number(self, number):
    if self.has_won:
      return False
    elif number in self.numbers:
      self.marks.append(self.numbers[number])

      if self.check_win():
        self.has_won = True
        self.winning_number = number
        return number

    return False

  @property
  def score(self):
    return sum(number for number, position in self.numbers.items() if not position in self.marks) * self.winning_number

def read_input():
  numbers, *cards = split_at(fileinput.input(), is_blank)

  numbers = list(map(int, numbers[0].split(",")))

  cards = [ Card.from_lines(card) for card in cards ]

  return numbers, cards

def part(part, numbers, cards):
  for number in numbers:
    for card in cards:
      if card.draw_number(number) is not False:
        if part == 1:
          return card.score
        else:
          winner = card

  return winner.score
        
def main():
  numbers, cards = read_input()

  print(part(1, numbers, cards))
  print()
  print(part(2, numbers, cards))

if __name__ == "__main__":
  main()
