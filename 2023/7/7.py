#!/usr/bin/python3

import fileinput

from collections import Counter
from itertools import combinations_with_replacement

# value of a card = CARDS.index(card)
CARDS = "23456789TJQKA"
CARDS_WITH_JOKERS = "J23456789TQKA"

JOKER = "J"

class Hand(str):
  J_is_Joker = False

  #def __new__(cls, src = None, bid = 0, *args, **kwargs):
  def __new__(cls, src, bid = 0, *args, **kwargs):
    self = super().__new__(cls, src, *args, **kwargs)

    self.bid = int(bid)

    if len(self) != 5 or any(card not in CARDS for card in self):
      raise ValueError
    
    return self

  def __repr__(self):
    return "Hand({}, bid = {})".format(super().__repr__(), self.bid)

  def __lt__(self, other):
    return self.signature < other.signature
  
  @property
  def kind(self):
    """
    map hand to its type represented by ordered numbers of unique cards

    provides natural sorting since lists are sorted lexically:

    >>> [1, 1, 1, 1, 1] < [2, 1, 1, 1] < [2, 2, 1] < [3, 1, 1] < [3, 2] < [4, 1] < [5]
    True
    >>> Hand("AAAAA").kind
    [5]
    >>> Hand("AAAKK").kind
    [3, 2]
    >>> Hand("23456").kind
    [1, 1, 1, 1, 1]
    """

    if Hand.J_is_Joker and JOKER in self:
      # given the scoring system, it's always the best strategy to replace both jokers with the same card
      # combinations = [ list(combo) for combo in combinations_with_replacement(CARDS_WITH_JOKERS[1:], self.count(JOKER)) ]
      # candidates = [ Hand("".join([combo.pop() if card == JOKER else card for card in self])) for combo in combinations ]
      stripped = Counter(self.replace(JOKER, ""))
      if stripped:
        replacement = stripped.most_common()[0][0]

        return Hand(self.replace(JOKER, replacement)).kind
      else:
        return Hand("AAAAA").kind
    else:
      return sorted(Counter(self).values(), reverse = True)

  @property
  def card_values(self):
    if Hand.J_is_Joker:
      base = CARDS_WITH_JOKERS
    else:
      base = CARDS
    return tuple(base.index(card) for card in self)

  @property
  def signature(self):
    return (self.kind, self.card_values)

def main():
  hands = [ Hand(*line.split()) for line in fileinput.input() ]

  # part 1
  print(sum(rank * hand.bid for rank, hand in enumerate(sorted(hands), 1)))

  # part 1
  Hand.J_is_Joker = True
  print(sum(rank * hand.bid for rank, hand in enumerate(sorted(hands), 1)))

if __name__ == "__main__":
  main()
