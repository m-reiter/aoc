#!/usr/bin/python3

import fileinput
import re
import operator
from itertools import combinations
from more_itertools import split_at, set_partitions
from collections import defaultdict

OPERATIONS = {
  "AND": operator.and_,
  "OR" : operator.or_,
  "XOR": operator.xor
}

GATE = re.compile("(.*) ([A-Z]*) (.*) -> (.*)")

def is_blank(line):
  return not(line.strip())
  
class MonitoringDevice:
  def __init__(self, inputlines):
    wires, gates = split_at(inputlines, is_blank)

    #self.wires = {}
    self.registers = defaultdict(list)

    for wire in wires:
      name, state = wire.strip().split(": ")
      #self.wires[name] = int(state)
      self.registers[name[0]].append(int(state))

    self.initial_x = self.x
    self.initial_y = self.y

    self.gates = defaultdict(list)
    self.outputs = set()
    for gate in gates:
      in1, operation, in2, out = GATE.match(gate).groups()
      self.gates[(in1, in2)].append((operation, out))
      self.outputs.add(out)
      if out.startswith("z"):
        self.registers["z"].append(None)

    self.swaps = set()

    self.reset()

  def reset(self, x = None, y = None):
    self.x = self.initial_x if x is None else x
    self.y = self.initial_y if y is None else y
    
    self.wires = {}
    for name in ("x", "y"):
      for position, value in enumerate(self.registers[name]):
        self.wires[f"{name}{position:02}"] = value

  def get_register(self, register):
    return sum(n * 2**i for i, n in enumerate(self.registers[register]))

  def set_register(self, register, value):
    for i in range(len(self.registers[register])):
      self.registers[register][i] = int(bool(value & (2**i)))

  @property
  def x(self):
    return self.get_register("x")

  @x.setter
  def x(self, value):
    self.set_register("x", value)

  @property
  def y(self):
    return self.get_register("y")

  @y.setter
  def y(self, value):
    self.set_register("y", value)

  @property
  def z(self):
    return self.get_register("z")

  def resolve(self):
    unresolved = set(self.gates.keys())
    while unresolved:
      resolvable = [ inputs for inputs in unresolved if all(input in self.wires for input in inputs) ]
      assert resolvable
      for inputs in resolvable:
        for operation, out in self.gates[inputs]:
          self.wires[out] = result = OPERATIONS[operation](*[self.wires[input] for input in inputs])
          if out.startswith("z"):
            self.registers["z"][int(out[1:])] = result
        unresolved.remove(inputs)
      handled_swaps = set()
      for swap in self.swaps:
        if all(output in self.wires for output in swap):
          out1, out2 = swap
          tmp = self.wires[out1]
          self.wires[out1] = self.wires[out2]
          self.wires[out2] = tmp
          handled_swaps.add(swap)
      self.swaps -= handled_swaps
    for i in range(len(self.registers["z"])):
      self.registers["z"][i] = self.wires[f"z{i:02}"]
    #assert not any(z is None for z in self.registers["z"])

  def correct(self):
  #  octets = list(combinations(self.outputs, 8))
  #  l = len(octets)
    for octet in combinations(self.outputs, 8):
    #for octet in enumerate(octets):
      #print(f"{i}/{l}", octet)
      print(octet)
      for swaps in set_partitions(octet, 4, min_size = 2, max_size = 2):
        self.swaps = set(map(tuple,swaps))
        self.reset()
        self.resolve()
        if self.x + self.y == self.z:
          print(swaps)
          return

def main():
  monitoringdevice = MonitoringDevice(fileinput.input())
  monitoringdevice.resolve()

  # part 1
  print(monitoringdevice.z)

  monitoringdevice.correct()

if __name__ == "__main__":
  main()
