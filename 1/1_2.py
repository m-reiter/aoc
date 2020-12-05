#!/usr/bin/python3

import fileinput

def main():

  numbers = set()
  sums = {}
  
  for line in fileinput.input():

    expense = int(line)
    
    for e2 in numbers:
      sums[expense+e2] = (expense,e2)

    numbers.add(expense)
    
    complement = 2020-expense
    
    if complement in sums.keys():
      break

  print(expense*sums[complement][0]*sums[complement][1])

if __name__ == "__main__":
  main()
