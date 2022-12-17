#!/usr/bin/python3

import fileinput
from more_itertools import pairwise
from collections import defaultdict

def read_polymer(data):
  polymer = data.readline().strip()
  data.readline()
  return polymer

def get_pair_counts(polymer):
  pair_counts = defaultdict(int)
  for pair in pairwise(polymer):
    pair_counts[pair] += 1
  return pair_counts

def parse_rules(data):
  rules = {}
  for line in data:
    combination,insert = line.strip().split(" -> ")
    rules[tuple(combination)] = insert
  return rules

def apply_rules(pair_counts,rules):
  new_pair_counts = defaultdict(int)
  for pair,count in pair_counts.items():
    insertion = rules.get(pair)
    if insertion:
      new_pair_counts[(pair[0],insertion)] += count
      new_pair_counts[(insertion,pair[1])] += count
    else:
      new_pair_counts[pair] += count
  return new_pair_counts

def solve_part(pair_counts,rules,polymer,n):
  for _ in range(n):
    pair_counts = apply_rules(pair_counts,rules)
  counts = sorted([(element,polymer.count(element)) for element in set(polymer)], key = lambda x: x[1])
  element_counts = defaultdict(int)
  element_counts[polymer[0]] += 1
  element_counts[polymer[-1]] += 1
  #print(element_counts)
  #print(pair_counts)
  for pair,count in pair_counts.items():
    element_counts[pair[0]] += count
    element_counts[pair[1]] += count

  return (max(element_counts.values())-min(element_counts.values()))//2,pair_counts

def main():
  data = fileinput.input()
  polymer = read_polymer(data)
  pair_counts = get_pair_counts(polymer)
  rules = parse_rules(data)

  part1,pair_counts = solve_part(pair_counts,rules,polymer,10)
  print(part1)

  part2,_ = solve_part(pair_counts,rules,polymer,30)
  print(part2)

if __name__ == "__main__":
  main()
