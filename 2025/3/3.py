#!/usr/bin/python3

import fileinput

def max_joltage(battery, n_digits):
  if n_digits == 1:
    return int(max(battery))

  left = max(battery[:-n_digits+1])

  return 10**(n_digits-1) * int(left) + max_joltage(battery[battery.index(left)+1:], n_digits-1)

def main():
  batteries = list(map(str.strip, fileinput.input()))

  # part 1
  print(sum(map(lambda x: max_joltage(x, 2), batteries)))

  # part 2
  print(sum(map(lambda x: max_joltage(x, 12), batteries)))

if __name__ == "__main__":
  main()
