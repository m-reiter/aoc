#!/usr/bin/python3

import fileinput

def normalize(range):
  first, last = range

  if len(first) % 2 != 0:
    first = "1" + len(first)*"0"

  if len(last) % 2 != 0:
    last = "9"*(len(last) - 1)

  return first, last

def find_invalids(normalized):
  first, last = normalized

  invalids = []

  digits = len(first)
  if len(last) < digits:
    return []

  lowerleft, lowerright = map(int,(first[:digits//2],first[digits//2:]))
  upperleft, upperright = map(int,(last[:digits//2],last[digits//2:]))
  
  for i in range(lowerleft, upperleft+1):
    candidate = int(f"{i}{i}")
    if int(first) <= candidate <= int(last):
      invalids.append(candidate)

  return invalids

def main():
  ranges = [ range.split("-") for range in fileinput.input().readline().strip().split(",") ]

  # part 1
  print(sum(map(sum,map(find_invalids,map(normalize, ranges)))))

if __name__ == "__main__":
  main()
