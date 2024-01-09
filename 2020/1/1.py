#!/usr/bin/python3

import fileinput

def main():

  numbers = set()
  sums = {}
  solution1 = None
  solution2 = None
  
  for line in fileinput.input():

    expense = int(line)
    
    for e2 in numbers:
      sums[expense+e2] = (expense,e2)

    complement = 2020-expense

    if complement in numbers:
      solution1 = expense*complement

    numbers.add(expense)
    
    if complement in sums.keys():
      solution2 = expense*sums[complement][0]*sums[complement][1]
      
    if solution1 and solution2:
      break

  print(solution1)
  print(solution2)

if __name__ == "__main__":
  main()
