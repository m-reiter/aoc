#!/usr/bin/python3

STEPS = 314
#STEPS = 3

def print_buffer(cbuffer,position,interval=None):
  if interval:
    region = enumerate(cbuffer[interval],interval.start)
  else:
    region = enumerate(cbuffer)
  print("".join(("({})" if i == position else " {} ").format(value) for i,value in region))

def main():

  # part 1
  cbuffer = [ 0 ]
  position = value = 0

  for _ in range(2017):
    value += 1
    position = (position + STEPS) % len(cbuffer) + 1
    cbuffer.insert(position, value)

  print_buffer(cbuffer,position,slice(position-3,position+4))

  # part 2
  cbuffer = [ 0 ]
  position = value = 0

  for _ in range(50000000):
    value += 1
    position = (position + STEPS) % value + 1
    if position == 1:
      cbuffer.insert(1,value)

  print_buffer(cbuffer,position)

if __name__ == "__main__":
  main()
