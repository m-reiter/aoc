#!/usr/bin/python3

import fileinput

def main():

  valid = 0

  for line in fileinput.input():

    (numbers, character, password) = line.split()

    numbers = list(map(int, numbers.split("-")))

    character = character[0]

    password = "x"+password

    if list(map(password.__getitem__, numbers)).count(character) == 1:

      valid += 1
      
  print(valid)

if __name__ == "__main__":
  main()
