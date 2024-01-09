#!/usr/bin/python3

import fileinput
from collections import Counter

def find_chains(adapters,start,goal):

  adapters = sorted(adapters)
  chains = [0]*len(adapters)

  for i in reversed(range(len(adapters))):
  
    if goal - adapters[i] <= 3:
      chains[i] = 1

    for j in range(i+1,min(i+4,len(adapters))):
      if adapters[j] - adapters[i] <= 3:
        chains[i] += chains[j]

  total = sum([chains[i] for i in range(3) if adapters[i] - start <=3])
      
  return total

def main():
  
  adapters = [int(line) for line in fileinput.input()]

  chain = [0] + sorted(adapters)
  chain.append(chain[-1]+3)

  differences = [chain[i]-chain[i-1] for i in range(1,len(chain))]

  counts = Counter(differences)
  
  print(counts[1]*counts[3])

  print(find_chains(adapters,0,max(adapters)+3))

if __name__ == "__main__":
  main()
