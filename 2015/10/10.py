#!/usr/bin/python3

from more_itertools import run_length

INPUT = "1321131112"

def look_and_say(string):
  return "".join(str(count)+value for value,count in run_length.encode(string))

def main():
  string = INPUT

  for _ in range(40):
    string = look_and_say(string)

  print(len(string))

  for _ in range(10):
    string = look_and_say(string)
    print(_, len(string))

  print(len(string))

if __name__ == "__main__":
  main()
