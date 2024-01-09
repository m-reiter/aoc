#!/usr/bin/python3

import fileinput
import re
from itertools import chain,combinations
from collections import defaultdict

CHIP = re.compile(" ([^ ]*)-compatible microchip")
GENERATOR = re.compile(" ([^ ]*) generator")

class Element():
  def __init__(self,name="unobtainium",generator=0,chip=0):
    self.name = name
    self.generator = generator
    self.chip = chip

  def __repr__(self):
    return "element {}: generator on floor {}, chip on floor {}".format(self.name,self.generator,self.chip)

  def tuple(self):
    return (self.generator,self.chip)

  def copy(self):
    return Element(self.name,self.generator,self.chip)

  def on_floor(self,floor):
    return [(self.name,kind) for kind in ("generator","chip") if self.__getattribute__(kind) == floor]

  def floor_string(self,floor):
    tmp = (self.name[0].upper()+"G ") if self.generator == floor else ".  "
    return tmp + ((self.name[0].upper()+"M") if self.chip == floor else ". ")

class State():
  def __init__(self):
    self.elevator = 1
    self.elements = defaultdict(Element)

  def __repr__(self):
    tmp = []
    for floor in range(4,0,-1):
      tmp.append("F{} {}  {}".format(floor,"E" if self.elevator == floor else "."," ".join(element.floor_string(floor) for element in self.elements.values())))
    return "\n".join(tmp)

  def hash(self):
    return (self.elevator,) + tuple(sorted(element.tuple() for element in self.elements.values()))

  def destinations(self):
    if self.elevator == 1:
      return [2]
    elif self.elevator == 4:
      return [3]
    else:
      return [self.elevator-1,self.elevator+1]

  def copy(self):
    new_state = State()
    new_state.elevator = self.elevator
    new_state.elements.update((key,value.copy()) for key,value in self.elements.items())
    return new_state

  def is_safe(self):
    for element in self.elements.values():
      if element.generator != element.chip and any(other.generator == element.chip for other in self.elements.values()):
        return False
    return True

  def is_final(self):
    return all(element.generator == element.chip == 4 for element in self.elements.values())

  def move(self,destination,items):
    for name,kind in items:
      self.elements[name].__setattr__(kind,destination)
    self.elevator = destination

  def get_moves(self):
    moves = []
    for floor in self.destinations():
      items = sum((element.on_floor(self.elevator) for element in self.elements.values()),[])
      for load in chain(combinations(items,1),combinations(items,2)):
        moves.append((floor,load))
    return moves

def parse_input():
  state = State()
  for floor,description in enumerate(fileinput.input(),1):
    chips = CHIP.findall(description)
    generators = GENERATOR.findall(description)
    for chip in chips:
      state.elements[chip].name = chip
      state.elements[chip].chip = floor
    for generator in generators:
      state.elements[generator].generator = floor
  return state
    
def solve(start):
  visited = {start.hash()}
  current = [(start,[])]
  moves = 0
  while True:
    new = []
    moves += 1
    for state,path in current:
      candidates = state.get_moves()
      for candidate in candidates:
        new_state = state.copy()
        new_state.move(*candidate)
        if new_state.is_final():
          return moves,path+[candidate]
        h = new_state.hash()
        if h not in visited and new_state.is_safe():
          new.append((new_state,path+[candidate]))
          visited.add(h)
    current = new

def play(start,path):
  state = start.copy()
  print("Initial state.")
  print(state)
  for move in path:
    print()
    print("Move {} to floor {}.".format(" and ".join(" ".join(description) for description in move[1]),move[0]))
    state.move(*move)
    print(state)
  print()
  print("All components on floor 4 after {} moves.".format(len(path)))

def main():
  start = parse_input()
  #moves,path = (solve(start))
  #play(start,path)
  start.elements["elerium"] = Element("elerium",1,1)
  start.elements["dilithium"] = Element("dilithium",1,1)
  moves,path = (solve(start))
  play(start,path)

if __name__ == "__main__":
  main()
