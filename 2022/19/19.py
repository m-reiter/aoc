#!/usr/bin/python3

import fileinput
import re

PATTERN = re.compile("Blueprint (\d+): Each ore robot costs (\d+) ore. Each clay robot costs (\d+) ore. Each obsidian robot costs (\d+) ore and (\d+) clay. Each geode robot costs (\d+) ore and (\d+) obsidian.")

class Resources(tuple):

  def __new__(cls,*args):
    return tuple.__new__(Resources,args)

  def __ge__(self,other):
    return all(a >= b for a,b in zip(self,other))

  def __lt__(self,other):
    return any(a < b for a,b in zip(self,other))

  def __le__(self,other):
    return all(a <= b for a,b in zip(self,other))

  def __add__(self,other):
    return Resources(*(a+b for a,b in zip(self,other)))

  def __sub__(self,other):
    return Resources(*(a-b for a,b in zip(self,other)))

SINGLES = [Resources(1,0,0,0),
           Resources(0,1,0,0),
           Resources(0,0,1,0),
           Resources(0,0,0,1)]

class Factory:
  def __init__(self,line):
    number,ore_ore,clay_ore,obsidian_ore,obsidian_clay,geode_ore,geode_obsidian = map(int,PATTERN.match(line).groups())
    self.number = number
    self.resources = Resources(0,0,0,0)
    self.robots = Resources(1,0,0,0)
    self.costs = (Resources(ore_ore,0,0,0),
                  Resources(clay_ore,0,0,0),
                  Resources(obsidian_ore,obsidian_clay,0,0),
                  Resources(geode_ore,0,geode_obsidian,0))
  
  def __lt__(self,other):
    if self.resources == other.resources and self.robots == other.robots:
      return False
    return other.resources >= self.resources and other.robots >= self.robots

  def copy(self):
    new = Factory.__new__(Factory)
    new.number = self.number
    new.resources = self.resources
    new.robots = self.robots
    new.costs = self.costs
    return new

  def step(self):
    new_states = []
    if any(self.resources < cost for cost in self.costs):
      new = self.copy()
      new.resources += new.robots
      new_states.append(new)
    for kind,cost in enumerate(self.costs):
      if self.resources >= cost:
        new = self.copy()
        new.resources -= cost
        new.resources += new.robots
        new.robots += SINGLES[kind]
        new_states.append(new)
    return [state for state in new_states if not any(state < other for other in new_states)]

  def __repr__(self):
    return "Factory #{}, robots = {}, resources = {}".format(self.number,self.robots,self.resources)
   
def part1(factories):
  for _ in range(24):
    print(_)
    new_states = []
    for factory in factories:
      new_states += factory.step()
      factories = new_states
    print(len(factories))
    #print(factories)


def main():
  factories = [Factory(line) for line in fileinput.input()]
  print(part1(factories[:1]))

if __name__ == "__main__":
  main()
