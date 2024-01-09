#!/usr/bin/python3

import fileinput
from collections import Counter,defaultdict

from P import P

UP = P(0,-1)
DOWN = P(0,1)
LEFT = P(-1,0)
RIGHT = P(1,0)

CARTS = {
  "^": (UP,"|"),
  "v": (DOWN,"|"),
  "<": (LEFT,"-"),
  ">": (RIGHT,"-")
}

CART_SYMBOLS = { value[0]: char for char,value in CARTS.items() }

TURNS = {
  (UP,"\\"): LEFT,
  (UP,"/"):  RIGHT,
  (DOWN,"\\"): RIGHT,
  (DOWN,"/"): LEFT,
  (LEFT,"\\"): UP,
  (LEFT,"/"): DOWN,
  (RIGHT,"\\"): DOWN,
  (RIGHT,"/"): UP
}

TRACKS = "-|"
BENDS = "/\\"
INTERSECTION = "+"

class Cart:

  directions = [ UP, RIGHT, DOWN, LEFT ] # in clockwise order
  turnings = [ -1, 0, 1 ] # left, straight, right

  def __init__(self,position,direction):
    self.position = position
    self.direction = direction
    self.turning = 0

  def __repr__(self):
    return "Cart at {}, moving {}".format(self.position, self.direction)

  def move(self,grid):
    self.position += self.direction
    if grid[self.position] in BENDS:
      self.direction = TURNS[(self.direction,grid[self.position])]
    elif grid[self.position] == INTERSECTION:
      current = Cart.directions.index(self.direction)
      new = (current + Cart.turnings[self.turning]) % 4
      self.direction = Cart.directions[new]
      self.turning += 1
      self.turning %= 3

def detect_collision(carts):
  positions = [cart.position for cart in carts]
  if len(set(positions)) == len(carts):
    return None
  return Counter(positions).most_common(1)[0][0]

def print_grid(grid,carts,dimensions):
  carts = { cart.position: cart.direction for cart in carts }
  for y in range(dimensions[1]):
    for x in range(dimensions[0]):
      if P(x,y) in carts:
        print(CART_SYMBOLS[carts[P(x,y)]],end='')
      else:
        print(grid[P(x,y)],end='')
    print()

def main():
  grid = defaultdict(lambda: " ")
  carts = []
  for y,line in enumerate(fileinput.input()):
    for x,char in enumerate(line.rstrip("\n")):
      if char in CARTS:
        direction,track = CARTS[char]
        carts.append(Cart(P(x,y),direction))
        grid[P(x,y)] = track
      else:
        grid[P(x,y)] = char
  dimensions = (x+1,y+1)
  print_grid(grid,carts,dimensions)

  while True:
    #print(".",end='')
    for cart in sorted(carts, key = lambda c: (c.position.y,c.position.x)):
      cart.move(grid)
      collision = detect_collision(carts)
      if collision:
        print(collision)
        carts = [cart for cart in carts if cart.position != collision]
        print_grid(grid,carts,dimensions)
        print()
    if len(carts) <= 1:
      break

  print(carts)

if __name__ == "__main__":
  main()
