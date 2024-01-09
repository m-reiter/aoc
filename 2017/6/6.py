#!/usr/bin/python3

INPUT = "2 8 8 5 4 2 3 1 5 5 1 2 15 13 5 14"
#INPUT = "0 2 7 0"

def main():
  memorybanks = list(map(int,INPUT.split()))
  
  #part 1
  seen = [ tuple(memorybanks) ]
  steps = 0
  number = len(memorybanks)
  while True:
    print(memorybanks)
    steps += 1
    highest = memorybanks.index(max(memorybanks))
    blocks = memorybanks[highest]
    memorybanks[highest] = 0
    for i in range(number):
      memorybanks[(highest + 1 + i) % number] += blocks // number + int(i < blocks % number)
    if tuple(memorybanks) in seen:
      break
    seen.append(tuple(memorybanks))
  print(steps)
  print(steps-seen.index(tuple(memorybanks)))
  
if __name__ == "__main__":
  main()
