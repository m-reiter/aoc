#!/usr/bin/python3

import fileinput

def is_valid_part1(phrase):
  words = phrase.split()
  return len(words) == len(set(words))

def is_valid_part2(phrase):
  words = ["".join(sorted(word)) for word in phrase.split()]
  return len(words) == len(set(words))

def main():
  phrases = [line.strip() for line in fileinput.input()]
  print(sum(is_valid_part1(phrase) for phrase in phrases))
  print(sum(is_valid_part2(phrase) for phrase in phrases))

if __name__ == "__main__":
  main()
