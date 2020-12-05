#!/usr/bin/python3

import fileinput

def main():

  numbers = set()
  
  for line in fileinput.input():

    expense = int(line)
    complement = 2020-expense
    
    if complement in numbers:
      break

    numbers.add(expense)
  
  print(complement*expense)

if __name__ == "__main__":
  main()
