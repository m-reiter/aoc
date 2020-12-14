#!/usr/bin/python3

import fileinput
from collections import defaultdict
import re

class Docker():

  def __init__(self):

    self.memory = defaultdict(int)

    self.setmask()

  def __iter__(self):

    return iter(self.memory.values())

  def setmask(self, mask = "X"*36):

    self.mask = mask
    self.setter = int(mask.replace("X","0"),2)
    self.clearer = int(mask.replace("X","1"),2)

  def get(self, address):

    return self.memory[address]

  def setmem(self, address, arg):

    arg = int(arg)

    arg |= self.setter
    arg &= self.clearer

    self.memory[address] = arg

  def mangle(self, address, floating_positions, i):

    a = list("{:036b}".format(address))
    i = "{:036b}".format(i)[-len(floating_positions):]

    for j in range(len(i)):

      a[floating_positions[j]] = i[j]

    return int("".join(a),2)

  def setmem2(self, address, arg):

    arg = int(arg)

    floating_positions = [ x.start() for x in re.finditer("X", self.mask) ]

    address |= self.setter

    for i in range(2**len(floating_positions)):

      self.memory[self.mangle(address, floating_positions, i)] = arg

  def execute(self, line, mode = 1):

    cmd,arg = line.strip().split(" = ")

    if cmd == "mask":

      self.setmask(arg)

    elif cmd.startswith("mem"):

      address = int(cmd.split("[")[1][:-1])

      if mode == 1:
        self.setmem(address, arg)
      else:
        self.setmem2(address, arg)


def main():
  
  input_ = list(fileinput.input())

  docker = Docker()
  
  for line in input_:

    docker.execute(line)

  print(sum(docker))

  docker = Docker()
  
  for line in input_:

    docker.execute(line, mode = 2)

  print(sum(docker))


if __name__ == "__main__":
  main()
