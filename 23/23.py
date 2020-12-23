#!/usr/bin/python3

import fileinput

# sample input

INPUT = "389125467"

# real input

# INPUT = "624397158"

class Cups:

  def __init__(self, input_, verbose = False):

    self.current = 0
    self.cups = []
    self.verbose = verbose

    for char in input_:
      self.cups.append(int(char)-1)

    self.max = max(self.cups) + 1

  def __str__(self):

    str_ = [str(i+1) for i in self.cups]
    str_[self.current] = "({})".format(str_[self.current])

    return " ".join(str_)
    
  def fillup(self, maximum):

    for i in range(max(self.cups)+1, maximum):

      self.cups.append(i)

    self.max = maximum

  def move(self):

    current = self.current
    aux = self.cups[current:]+self.cups[:current]

    picked = aux[1:4]
    remainder = aux[4:]

    destination = (aux[0] - 1) % self.max

    while not destination in remainder:

      destination = (destination - 1) % self.max

    if self.verbose:
    
      print("cups:  {}".format(str(self)))
      print("pick up: {}".format(", ".join([str(i+1) for i in picked])))
      print("destination: {}".format(str(destination+1)))

    index = remainder.index(destination) + 1

    cups = aux[:1] + remainder[:index] + picked + remainder[index:]

    self.cups = cups[-current:] + cups[:-current]

    self.current = (current + 1) % len(self.cups)

  def labels(self):

    start = self.cups.index(0)

    return "".join(str(i+1) for i in self.cups[start+1:]+self.cups[:start])


def main():
  
  cups = Cups(INPUT)

  for i in range(100):

    cups.move()

  print(cups.labels())

  return True

  cups = Cups(INPUT)

  cups.fillup(1000000)

  for i in range(10000000):

    cups.move()

  i = cups.cups.index(0)
  c1 = cups.cups[i+1]
  c2 = cups.cups[i+2]

  print(c1)
  print(c2)
  print(c1*c2)


if __name__ == "__main__":
  main()
