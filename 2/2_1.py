#!/usr/bin/python3

import fileinput

def main():

  valid = 0

  for line in fileinput.input():

    (numbers, character, password) = line.split()

    (minnum, maxnum) = map(int, numbers.split("-"))

    character = character[0]

    if minnum <= password.count(character) <= maxnum:

      valid += 1
      
  print(valid)

if __name__ == "__main__":
  main()
