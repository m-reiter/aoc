#!/usr/bin/python3

import fileinput
from numpy import sign

from P import P

DIRECTIONS = {
  'U': P((0,1)),
  'D': P((0,-1)),
  'L': P((-1,0)),
  'R': P((1,0))
}

def get_move(H,T):
  diff = dx,dy = H + -1*T
  if max(abs(coord) for coord in diff) <2:
    return P((0,0))
  return P((sign(dx),sign(dy)))

def main():
  moves = [line.strip() for  line in fileinput.input()]
  
  # part 1
  
  H = P((0,0))
  T = P((0,0))
  visited = set()
  visited.add(T)
  
  for move in moves:
    direction,steps = move.split()

    for _ in range(int(steps)):
      H += DIRECTIONS[direction]
      T += get_move(H,T)
      visited.add(T)

  print(len(visited))

  # part 2
  
  rope = [P((0,0))] * 10
  visited = set()

  for move in moves:
    direction,steps = move.split()

    for _ in range(int(steps)):
      new_rope = [rope[0]+DIRECTIONS[direction]]
      for knot in rope[1:]:
        new_rope.append(knot+get_move(new_rope[-1],knot))
      rope = new_rope
      visited.add(rope[-1])

    #print(rope)

  print(len(visited))

if __name__ == "__main__":
  main()
