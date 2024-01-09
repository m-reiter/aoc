#!/usr/bin/python3

import fileinput

TESTCASES = [
  (3,5,8,4),
  (122,79,57,-5),
  (217,196,39,0),
  (101,153,71,4)
]

SERIAL = 5719

def calculate_powerlevel(x,y,serial):
  rack_id = x+10
  powerlevel = rack_id*y+serial
  powerlevel *= rack_id
  powerlevel = powerlevel % 1000 // 100 - 5
  return powerlevel

def main():
  for x,y,serial,result in TESTCASES:
    assert(calculate_powerlevel(x,y,serial) == result)

  grid = { (x,y,1): calculate_powerlevel(x,y,SERIAL) for x in range(1,301) for y in range(1,301) }

  for size in range(2,301):
    print(size)
    for x in range(1,301-size):
      for y in range(1,301-size):
        grid[(x,y,size)] = grid[(x,y,size-1)]
        for X in range(x,x+size):
          grid[(x,y,size)] += grid[(X,y+size-1,1)]
        for Y in range(y,y+size-1):
          grid[(x,y,size)] += grid[(x+size-1,Y,1)]

  best_area = max(grid, key = lambda x: grid[x])

  grid_3 = { key[:2]: value for key,value in grid.items() if key[2] == 3 }
  best_area_3 = max(grid_3, key = lambda x: grid_3[x])

  print(best_area_3)
  print(best_area)

if __name__ == "__main__":
  main()
