#!/usr/bin/python3

import fileinput
import re

PATTERN = re.compile("Valve ([A-Z]+) has flow rate=(\d+); tunnels? leads? to valves? ([A-Z, ]+)")
START = "AA"
DEAD_END = "XXX"

class State:
  
  def __init__(self,valves,positions=None,flow_rate=0,released=0,opened=set(),valid=0,elephant=False):
    self.valves = valves
    if positions is None:
      if elephant:
        self.positions = [START,START]
      else:
        self.positions = [START]
    else:
      self.positions = positions
    self.flow_rate = flow_rate
    self.released = released
    self.opened = opened
    self.valid = valid
  
  def get_moves(self,position):
    _,tunnels = self.valves[position]
    moves = ["move {} {}".format(position,tunnel) for tunnel in tunnels]
    if position not in self.opened:
      moves.append("open {}".format(position))
    return moves
    
  def tick(self):
    if len(self.opened) == self.valid:
      self.released += self.flow_rate
      return [self]
    #print("tick:",self)
    my_moves = self.get_moves(self.positions[0])
    print("***")
    print(my_moves)
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
  #      if not any(tunnel == visited and self.flow_rates[-1] == old_flow_rate for visited,old_flow_rate in zip(self.path,self.flow_rates)):
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

def run_part(valves,valid,turns,elephant=False):
  states = [State(valves,valid=valid,elephant=elephant)]
  for turn in range(turns):
    print(turn)
    new_states = []
    for state in states:
      new_states += state.tick()
    best = sorted(new_paths, key = lambda x: x.released + (30-turn) * x.flow_rates[-1], reverse = True)
    paths = best[:1000]
    print(len(paths))
  print(max(paths,key = lambda x: x.released))
  return max(path.released for path in paths)
  
def main():
  valves,valid = read_input()

  print(run_part(valves,valid,30))

if __name__ == "__main__":
  main()
