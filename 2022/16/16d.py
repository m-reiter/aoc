#!/usr/bin/python3

import fileinput
import re
from collections import defaultdict
from copy import deepcopy

PATTERN = re.compile("Valve ([A-Z]+) has flow rate=(\d+); tunnels? leads? to valves? ([A-Z, ]+)")
START = "AA"
DEAD_END = "XXX"

class State:
  
  def __init__(self,valves,positions=None,flow_rate=[0,0],previous=[defaultdict(lambda: -1) for _ in (0,1)],released=0,opened=set(),valid=0,elephant=False):
    self.valves = valves
    if positions is None:
      if elephant:
        self.positions = [START,START]
      else:
        self.positions = [START]
    else:
      self.positions = positions
    self.flow_rate = flow_rate
    self.previous = previous
    self.released = released
    self.opened = opened
    self.valid = valid
  
  def __hash__(self):
    return hash((tuple(sorted(self.positions)),tuple(sorted(self.opened)),self.released))

  def __gt__(self,other):
    gt = self.released > other.released
    gt &= sorted(self.positions) == sorted(other.positions)
    gt &= self.opened == other.opened
    return gt

  def get_moves(self,elephant=False):
    position = self.positions[elephant]
    flow_rate,tunnels = self.valves[position]
    moves = ["move {} {}".format(position,tunnel) for tunnel in tunnels if self.flow_rate[elephant] > self.previous[elephant][tunnel]]
    if position not in self.opened and flow_rate > 0:
      moves.append("open {}".format(position))
    return moves
    
  def tick(self):
    if len(self.opened) == self.valid:
      self.released += sum(self.flow_rate)
      return [self]
    my_moves = self.get_moves()
    states = [self.do_move(move) for move in my_moves]
    if len(self.positions) ==  1:
      return states
    final_states = []
    for state in states:
      elephant_moves = state.get_moves(elephant=True)
      for move in elephant_moves:
        final_states.append(state.do_move(move,elephant=True))
    return final_states

  def do_move(self,move,elephant=False):
    new_state = deepcopy(self)
    if not elephant:
      new_state.released += sum(new_state.flow_rate)
    cmd,*args = move.split()
    if cmd == "open":
      new_state.opened.add(args[0])
      flow_rate,_ = new_state.valves[args[0]]
      new_state.flow_rate[elephant] += flow_rate
    elif cmd == "move":
      start,destination = args
      assert new_state.positions[elephant] == start
      new_state.positions[elephant] = destination
      new_state.previous[elephant][destination] = new_state.flow_rate[elephant]
    return new_state

  def __repr__(self):
    return "Path: flow_rate {}, released {} positions {}".format(self.flow_rate,self.released,self.positions)
 
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
    print("* turn ",turn)
    print("*** ",len(states)," states")
    new_states = set()
    for state in states:
      new_states |= set(state.tick())
    print("*** ",len(new_states)," new states")
    #states = [state for state in new_states if not any(other > state for other in new_states)] 
    #print("*** after eliminating lesser states: ",len(states))
    best = sorted(new_states, key = lambda x: x.released + (turns-turn) * sum(x.flow_rate), reverse = True)
    print("*** sorting finished")
    states = best[:10000]
  print(max(states,key = lambda x: x.released))
  return max(state.released for state in states)
  
def main():
  valves,valid = read_input()

  #print(run_part(valves,valid,30))
  print(run_part(valves,valid,turns=26,elephant=True))

if __name__ == "__main__":
  main()
