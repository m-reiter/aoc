#!/usr/bin/python3

import fileinput

def main():
  changes = list(map(int,fileinput.input()))
  print(sum(changes))

  seen = {0}
  current = 0
  found = False

  while True:
    for change in changes:
      print("{} + {} = {}".format(current,change,current+change))
      current += change
      if current in seen:
        found = True
        break
      seen.add(current)
    if found:
      break

  print(current)

if __name__ == "__main__":
  main()
