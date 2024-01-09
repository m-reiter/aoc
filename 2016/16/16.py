#!/usr/bin/python3

from more_itertools import chunked

TRANSLATE = str.maketrans("01","10")
INPUT = "10111011111001111"

def dragon_curve(string,length):
  while len(string) < length:
    string = string+"0"+string[::-1].translate(TRANSLATE)
  return string[:length]

def checksum(string):
  while len(string) % 2 == 0:
    print(len(string))
    string = "".join("1" if len(set(pair)) == 1 else "0" for pair in chunked(string,2))
  return string
    
def main():
  print(checksum(dragon_curve(INPUT,272)))
  print(checksum(dragon_curve(INPUT,35651584)))

if __name__ == "__main__":
  main()
