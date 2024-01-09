#!/usr/bin/python3

import fileinput
from more_itertools import split_at

class Combat:

  def __init__(self, input_, recursive = False):

    self.players = []
    self.decks = []
    self.winner = None
    self.recursive = recursive

    if recursive:
      self.previous_positions = set()

    for player in split_at(input_, lambda x: not x.strip()):

      deck = []
        
      for line in player:

        if line.startswith("Player"):
          
          self.players.append(line.split()[1].strip(":\n"))

        else:

          deck.append(int(line))

      self.decks.append(deck)

  def score(self):

    score = 0

    for i in range(1,len(self.decks[self.winner])+1):

      score += i * self.decks[self.winner][-i]

    return score

  def round(self):

    if self.recursive:

      positions = set(player+":"+",".join(str(card) for card in deck) for player, deck in zip(self.players,self.decks))

      if positions & self.previous_positions:

        self.winner = 0

        return (self.winner, self.score())
      
      else:

        self.previous_positions |= positions

    current_cards = [deck.pop(0) for deck in self.decks]

    if self.recursive and all(card <= len(deck) for card, deck in zip(current_cards, self.decks)):
    
      winner = SubGame(self, current_cards).play()[0]
    
    else:
    
      winner = current_cards.index(max(current_cards))

    self.decks[winner] += [current_cards[i] for i in (winner, 1 - winner)]

    if 0 in [len(deck) for deck in self.decks]:

      self.winner = winner

      return (winner, self.score())

    else:

      return False

  def play(self):

    finished = self.round()

    while not finished:

      finished = self.round()

    return finished

class SubGame(Combat):

  def __init__(self, game, current_cards):

    self.players = game.players
    self.decks = [deck[:card] for deck, card in zip(game.decks, current_cards)]
    self.winner = None
    self.recursive = True
    self.previous_positions = set()


def main():
  
  game = Combat(fileinput.input())

  result = game.play()

  print(result[1])
  
  game = Combat(fileinput.input(), recursive = True)

  result = game.play()

  print(result[1])

if __name__ == "__main__":
  main()
