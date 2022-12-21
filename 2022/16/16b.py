#!/usr/bin/python3

import fileinput
import re

PATTERN = re.compile("Valve ([A-Z]+) has flow rate=(\d+); tunnels? leads? to valves? ([A-Z, ]+)")
START = "AA"
DEAD_END = "XXX"

class Path:
  
  def __init__(self,path=[START],flow_rates=[0],released=0,current=START,opened=0,valid=0):
    self.path = path
    self.flow_rates = flow_rates
    self.released = released
    self.current = current
    self.opened = opened
    self.valid = valid
  
  def tick(self,valves):
    #print("tick:",self)
    self.released += self.flow_rates[-1]
    if self.path[-1] == DEAD_END or self.opened == self.valid:
      return [self]
    new_paths = []
    flow_rate,tunnels = valves[self.current]
    #print(flow_rate,self.current,self.path)
    if self.opened < self.valid:
      if flow_rate > 0 and open_valve(self.current) not in self.path:
        new_paths.append(Path(self.path+[open_valve(self.current)],
                              self.flow_rates+[self.flow_rates[-1]+flow_rate],
                              self.released,self.current,self.opened+1,self.valid))
      for tunnel in tunnels:
        if not any(tunnel == visited and self.flow_rates[-1] == old_flow_rate for visited,old_flow_rate in zip(self.path,self.flow_rates)):
          new_paths.append(Path(self.path+[tunnel],self.flow_rates+[self.flow_rates[-1]],self.released,tunnel,self.opened,self.valid))
    #print(new_paths)
    if len(new_paths) == 0:
      new_paths.append(Path(self.path+[DEAD_END],self.flow_rates+[self.flow_rates[-1]],self.released,self.current,self.opened,self.valid))
    return new_paths

  def __repr__(self):
    return "Path: flow_rate {}, released {}, trace: {}".format(self.flow_rates[-1],self.released,list(zip(self.path,self.flow_rates)))
 
def open_valve(name):
  return "Open valve {}".format(name)

def read_input():
  valves = {}
  valid_valves = 0
  for line in fileinput.input():
    name,flow_rate,tunnels = PATTERN.match(line).groups()
    flow_rate = int(flow_rate)
    tunnels = tunnels.split(", ")
    valves[name] = (flow_rate,tunnels)
    if flow_rate > 0:
      valid_valves += 1
  return valves,valid_valves

def part1(valves,valid):
  paths = [Path(valid=valid)]
  for _ in range(30):
    print(_)
    new_paths = []
    for path in paths:
      new_paths += path.tick(valves)
    best = max(new_paths, key = lambda x: x.released)
    if best.opened == valid:
      paths = [best]
    else:
      paths = new_paths
  print(max(paths,key = lambda x: x.released))
  return max(path.released for path in paths)
  
def main():
  valves,valid = read_input()

  print(part1(valves,valid))

if __name__ == "__main__":
  main()
