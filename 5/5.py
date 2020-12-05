#!/usr/bin/python3

import fileinput

def parse_code(code):
  row = int(code[0:7].replace("F","0").replace("B","1"),2)
  seat = int(code[7:10].replace("L","0").replace("R","1"),2)
  seatID = row*8+seat
  return (row,seat,seatID)

def find_seat(seats):
  ids = set([ seat[2] for seat in seats ])
  return set(range(min(ids),max(ids)+1))-ids

def main():
  seats = [ parse_code(line) for line in fileinput.input() ]

  s1 = max(seats, key=lambda seat: seat[2])

  print(s1)

  s2 = find_seat(seats)

  print(s2)

if __name__ == "__main__":
  main()
