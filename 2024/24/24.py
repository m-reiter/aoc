#!/usr/bin/python3

import fileinput
import re
import operator
from more_itertools import split_at
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

    self.wires = {}

    for wire in wires:
      name, state = wire.strip().split(": ")
      self.wires[name] = int(state)

    self.gates = defaultdict(list)
    self.z_wires = []
    for gate in gates:
      in1, operation, in2, out = GATE.match(gate).groups()
      self.gates[(in1, in2)].append((operation, out))
      if out.startswith("z"):
        self.z_wires.append(None)

  def resolve(self):
    unresolved = set(self.gates.keys())
    while unresolved:
      resolvable = [ inputs for inputs in unresolved if all(input in self.wires for input in inputs) ]
      assert resolvable
      for inputs in resolvable:
        for operation, out in self.gates[inputs]:
          self.wires[out] = result = OPERATIONS[operation](*[self.wires[input] for input in inputs])
          if out.startswith("z"):
            self.z_wires[int(out[1:])] = result
        unresolved.remove(inputs)
    assert not any(z is None for z in self.z_wires)

def main():
  monitoringdevice = MonitoringDevice(fileinput.input())
  monitoringdevice.resolve()

  # part 1
  print(sum(z * 2**n for n, z in enumerate(monitoringdevice.z_wires)))

if __name__ == "__main__":
  main()
