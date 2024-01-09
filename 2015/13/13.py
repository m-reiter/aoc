#!/usr/bin/python3

import fileinput
import re

from itertools import permutations
from collections import defaultdict

PATTERN = re.compile("(\w+) would (gain|lose) (\d+) happiness units by sitting next to (\w+).")

def calculate_preferences(stream):
  preferences = defaultdict(int)

  for line in stream:
    attendee, gain_lose, amount, neighbor = PATTERN.match(line).groups()

    preferences[(attendee, neighbor)] = int(amount) * (-1 if gain_lose == "lose" else 1)

  return preferences
  
def calculate_happiness(order, preferences):
  happiness = 0
  for position, attendee in enumerate(order[:-1]):
    happiness += preferences[(attendee, order[position - 1])]
    happiness += preferences[(attendee, order[position + 1])]
  happiness += preferences[(order[-1],order[-2])]
  happiness += preferences[(order[-1],order[0])]

  return happiness

def main():
  preferences = calculate_preferences(fileinput.input())

  attendees = set(pair[0] for pair in preferences)
  
  best_order = max(permutations(attendees), key = lambda x: calculate_happiness(x, preferences))
  print(best_order)
  print(calculate_happiness(best_order, preferences))

  attendees.add("me")

  best_order = max(permutations(attendees), key = lambda x: calculate_happiness(x, preferences))
  print(best_order)
  print(calculate_happiness(best_order, preferences))

if __name__ == "__main__":
  main()
