#!/usr/bin/python3

# sample input

INPUT = "389125467"

# real input

INPUT = "624397158"

class Cups:

  def __init__(self, input_, ncups = None, verbose = False):

    self.nextcup = {}
    self.verbose = verbose
    self.move_ = 0

    cups = [int(char) - 1 for char in input_]

    self.current = first = cups[0]
    last = cups[-1]

    for i in range(len(cups)):

      self.nextcup[cups[i]] = cups[(i+1) % len(cups)]

    self.max = max(cups) + 1

    if ncups is not None:

      self.nextcup[ncups - 1] = first
      self.nextcup[last] = self.max
      self.max = ncups

  def __repr__(self):

    str_ = "cups: ({})".format(self.current + 1)

    key = self.nextcup[self.current]

    while key in self.nextcup and key != self.current:

      str_ += " {}".format(str(key + 1))

      key = self.nextcup[key]

    return str_
    
  def next(self, start):

    return self.nextcup.get(start, start + 1)

  def move(self):

    if self.verbose:

      self.move_ += 1

      print("\n-- move {} --".format(self.move_))
      print(self)

    picked = [self.next(self.current)]

    for i in range(2):

      picked.append(self.next(picked[-1]))

    self.nextcup[self.current] = self.next(picked[-1])

    destination = (self.current - 1) % self.max

    while destination in picked:

      destination = (destination - 1) % self.max

    if self.verbose:
    
      print("pick up: {}".format(", ".join([str(i+1) for i in picked])))
      print("destination: {}".format(str(destination+1)))

    self.nextcup[picked[-1]] = self.next(destination)
    self.nextcup[destination] = picked[0]

    self.current = self.next(self.current)

  def labels(self):

    start = self.nextcup[0]

    labels = ""

    while start != 0:

      labels += str(start + 1)
      start = self.nextcup[start]

    return labels


def main():
  
  cups = Cups(INPUT, verbose = True)

  for i in range(100):

    cups.move()

  print("\n-- final --")
  print(cups)

  print()

  print(cups.labels())

#  return True

  cups = Cups(INPUT, ncups = 1000000)

  for i in range(10000000):

    cups.move()

  c1 = cups.next(0) + 1
  c2 = cups.next(c1 - 1) + 1

  print(c1)
  print(c2)
  print(c1*c2)


if __name__ == "__main__":
  main()
