#!/usr/bin/python3

import fileinput
import re

CONTAINERRE = re.compile("(.*?) bag")
CONTENTRE = re.compile("(\d+) (.*?) bag")

class Rules():

  def __init__(self):

    self.colors = set()
    self.contents = {}
    self.containers = {}

    for line in fileinput.input():

      container = CONTAINERRE.match(line).group(1)

      self.colors.add(container)

      self.contents[container] = {}

      for match in CONTENTRE.finditer(line):

        number = int(match.group(1))
        color = match.group(2)
        
        self.colors.add(color)

        self.contents[container][color] = number

        if color not in self.containers.keys():
          self.containers[color] = set()

        self.containers[color].add(container)

  def find_containers(self, color):

    if color not in self.containers.keys():
      return set()

    containers = self.containers[color]

    for color in list(containers):
      containers |= self.find_containers(color)

    return containers

  def number_of_bags_in(self, color):

    if color not in self.contents.keys():
      return 0

    number_of_bags = sum(self.contents[color].values())

    for color,number in self.contents[color].items():
      number_of_bags += number*self.number_of_bags_in(color)

    return number_of_bags

def main():
  
  rules = Rules()
  
  print(len(rules.find_containers("shiny gold")))

  print(rules.number_of_bags_in("shiny gold"))

if __name__ == "__main__":
  main()
