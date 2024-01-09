#!/usr/bin/python3

import sys

class Marble:
  def __init__(self,number=0,clockwise=None,ccw=None):
    self.number = number
    self.clockwise = self if clockwise is None else clockwise
    self.ccw = self if ccw is None else ccw 

def main():
  NPLAYERS = 9 if len(sys.argv) < 2 else int(sys.argv[1])
  LAST_MARBLE = 25 if len(sys.argv) < 3 else int(sys.argv[2])

  scores = [0] * NPLAYERS
  zero = current = Marble()

  for n in range(LAST_MARBLE):
    player = n % NPLAYERS
    value = n+1
    if value % 23:
      left = current.clockwise
      right = left.clockwise
      current = Marble(value,right,left)
      left.clockwise = right.ccw = current
    else:
      for _ in range(7):
        current = current.ccw
      scores[player] += value + current.number
      current.ccw.clockwise = current.clockwise
      current.clockwise.ccw = current.ccw
      current = current.clockwise
      
  print(max(scores))

if __name__ == "__main__":
  main()
