#!/usr/bin/python3

import string

from more_itertools import windowed

CURRENT = "vzbxkghb"
CURRENT = "vzbxxyzz"

TWENTYSIX = (string.digits + string.ascii_lowercase)[:26]

DECODE = str.maketrans(string.ascii_lowercase, TWENTYSIX)

SEQUENCES = ["".join(sequence) for sequence in windowed(string.ascii_lowercase,3)]
FORBIDDEN = "iol"
PAIRS = [char+char for char in string.ascii_lowercase]

def is_valid(password):
  if any(character in password for character in FORBIDDEN):
    return False
  if not any(sequence in password for sequence in SEQUENCES):
    return False
  return sum(pair in password for pair in PAIRS) >= 2

def encode(password):
  digits = []

  for _ in range(8):
    password, digit = divmod(password, 26)
    digits.append(digit)

  digits.reverse()

  return "".join(string.ascii_lowercase[d] for d in digits)

def increase(password):
  password = int(password.translate(DECODE),26)

  return encode(password + 1)

def main():
  password = increase(CURRENT)

  while not is_valid(password):
    password = increase(password)

  print(password)
  
if __name__ == "__main__":
  main()
