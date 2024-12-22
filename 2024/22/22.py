#!/usr/bin/python3

import fileinput
from collections import defaultdict
from more_itertools import windowed, pairwise

MODULO = 16777216

def mix_and_prune(secret, number):
  return (secret ^ number) % MODULO

def evolve(buyers):
  tmp_results = [ mix_and_prune(buyer[-1], buyer[-1] * 64) for buyer in buyers ]
  tmp_results = [ mix_and_prune(tmp_result, tmp_result // 32) for tmp_result in tmp_results ]
  buyers = [ buyer + [ mix_and_prune(tmp_result, tmp_result * 2048) ] for buyer, tmp_result in zip(buyers, tmp_results) ]
  return buyers

def main():
  buyers = [ [ int(line) ] for line in fileinput.input() ]

  # part 1
  for _ in range(2000):
    buyers = evolve(buyers)
    print(len(buyers[0]))
  print(sum(buyer[-1] for buyer in buyers))
  
  # part 2
  sequence_to_prices = defaultdict(list)
  for buyer in buyers:
    s_to_p = {}
    prices = [ price % 10 for price in buyer ]
    differences = [ b - a for a, b in pairwise(prices) ]
    for sequence, price in zip(windowed(differences, 4), prices[4:]):
      if sequence not in s_to_p:
        s_to_p[sequence] = price
    for sequence, price in s_to_p.items():
      sequence_to_prices[sequence].append(price)
  best_sequence = max(sequence_to_prices, key = lambda sequence: sum(sequence_to_prices[sequence]))
  print(best_sequence)
  print(sequence_to_prices[best_sequence])
  print(sum(sequence_to_prices[best_sequence]))

if __name__ == "__main__":
  main()
