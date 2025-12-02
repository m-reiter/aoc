#!/usr/bin/python3

import fileinput

def normalize(interval):
  first, last = interval

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

def find_invalids_2(interval):
  first, last = interval

  digits = len(first)
  if len(last) > digits:
    return find_invalids_2((first, "9"*digits)) | find_invalids_2(("1"+"0"*digits, last))

  invalids = set()

  for l in range(1, digits):
    times, remainder = divmod(digits, l)
    if remainder == 0:
      for i in range(10**(l-1), 10**l):
        candidate = int(str(i)*times)
        if int(first) <= candidate <= int(last):
          invalids.add(candidate)

  return invalids


def main():
  intervals = [ interval.split("-") for interval in fileinput.input().readline().strip().split(",") ]

  # part 1
  print(sum(map(sum,map(find_invalids,map(normalize, intervals)))))

  # part 2
  print(sum(map(sum,map(find_invalids_2, intervals))))

if __name__ == "__main__":
  main()
