#!/usr/bin/python3

import fileinput
from collections import Counter

def read_data():
  return list(map(str.strip,fileinput.input()))

def main():
  data = read_data()
  print("".join(Counter(position).most_common(1)[0][0] for position in zip(*data)))
  print("".join(Counter(position).most_common()[-1][0] for position in zip(*data)))

if __name__ == "__main__":
  main()
