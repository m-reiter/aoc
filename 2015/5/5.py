#!/usr/bin/python3

import fileinput
import re

TEST_CASES = {
  "ugknbfddgicrmopn": True,
  "aaa": True,
  "jchzalrnumimnmhp": False,
  "haegwjzuvuyypxyu": False,
  "dvszwmarrgswjxmb": False
}

TEST_CASES_2 = {
  "qjhvhtzxzqqjkmpb": True,
  "xxyxx": True,
  "uurcxstgmygtbstg": False,
  "ieodomkazucvgmuy": False
}

NAUGHTY = [ "ab", "cd", "pq", "xy" ]

VOWEL = re.compile("[aeiou]")
TWICE = re.compile("(.)\\1")

REPEATED_PAIR = re.compile("(..).*\\1")
ONE_BETWEEN = re.compile("(.).\\1")

def is_nice(string):
  if any(naughty in string for naughty in NAUGHTY):
    return False
  if len(VOWEL.findall(string)) < 3:
    return False
  if not TWICE.search(string):
    return False
  return True

def is_nice_2(string):
  if not REPEATED_PAIR.search(string):
    return False
  if not ONE_BETWEEN.search(string):
    return False
  return True

def main():
  for string,nice in TEST_CASES.items():
    assert is_nice(string) == nice

  strings = [ line.strip() for line in fileinput.input() ]

  print(sum(map(is_nice,strings)))

  for string,nice in TEST_CASES_2.items():
    assert is_nice_2(string) == nice

  print(sum(map(is_nice_2,strings)))

if __name__ == "__main__":
  main()
