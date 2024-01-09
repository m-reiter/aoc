#!/usr/bin/python3

import fileinput

class Group():
  
  def __init__(self,answers):
    
    self.any = set()
    self.all = set(answers[0])

    for line in answers:
      self.any |= set(line)
      self.all &= set(line)

    self.members = len(answers)

  @property
  def numany(self):
    return len(self.any)

  @property
  def numall(self):
    return len(self.all)


def parse_groups():

  groups = []

  answers = []

  for line in fileinput.input():

    if line.strip():
      answers.append(line.strip())
    else:
      groups.append(Group(answers))
      answers = []

  groups.append(Group(answers))

  return groups


def main():

  groups = parse_groups()

  print(sum([group.numany for group in groups]))

  print(sum([group.numall for group in groups]))


if __name__ == "__main__":
  main()
