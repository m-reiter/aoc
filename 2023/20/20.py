#!/usr/bin/python3

import fileinput

from enum import IntEnum
from attr import attrs, attrib
from collections import deque
from functools import reduce
from operator import mul
from math import gcd

def lcm(a, b):
  return a * b // gcd(a, b)

class Signal(IntEnum):
  low = 0
  high = 1

@attrs
class Module:
  name = attrib()
  outputs = attrib(factory = list)

  def connect_from(self, sender):
    pass

  def connect_to(self, receiver):
    self.outputs.append(receiver)

  def emit(self, signal):
    return (self.name, signal, tuple(self.outputs))

  def handle(self, sender, signal):
    pass

  def reset(self):
    pass

  @property
  def is_initial(self):
    return True

  def __str__(self):
    return ""

@attrs
class FlipFlop(Module):
  is_on = attrib(default  = False)

  def handle(self, sender, signal):
    if signal == Signal.low:
      self.is_on = not self.is_on
      
      return self.emit(Signal.high if self.is_on else Signal.low)

  def reset(self):
    self.is_on = False

  @property
  def is_initial(self):
    return self.is_on == False

  def __str__(self):
    return "{}:{}".format(self.name, "I" if self.is_on else "_")

@attrs
class Conjunction(Module):
  previous = attrib(factory = dict)

  def connect_from(self, sender):
    self.previous[sender] = Signal.low

  def handle(self, sender, signal):
    self.previous[sender] = signal

    return self.emit(Signal.low if all(s == Signal.high for s in self.previous.values()) else Signal.high)

  def reset(self):
    self.previous = { sender: Signal.low for sender in self.previous }

  @property
  def is_initial(self):
    return all(signal == Signal.low for signal in self.previous.values())

  def __str__(self):
    return "{}:{}".format(self.name, "".join("I" if self.previous[s] else "_" for s in sorted(self.previous)))

class Broadcaster(Module):
  def handle(self, sender, signal):
    return self.emit(signal)

MODULES = {
  "%": FlipFlop,
  "&": Conjunction
}

@attrs
class Machines:
  modules = attrib(factory = dict)
  all_modules = attrib(factory = dict)
  subsets = attrib(factory = list)
  presses = attrib(default = 0)
  emitted = attrib(default = [0, 0])
  cycle = attrib(default = None)

  def reset(self):
    for module in self.modules.values():
      module.reset()
    self.presses = 0
    self.emitted = [0, 0]
  
  @property
  def is_initial(self):
    return all(module.is_initial for module in self.modules.values())

  def add_module(self, module):
    self.modules[module.name] = module

  def connect_inputs(self):
    senders = list(self.modules.values())
    for sender in senders:
      for receiver in sender.outputs:
        if not receiver in self.modules:  
          self.add_module(Module(receiver))

        self.modules[receiver].connect_from(sender.name)

    self.all_modules = self.modules

  def press_button(self, verbose = True):
    signal_queue = deque([ ("button", Signal.low, [ "broadcaster" ]) ])

    while signal_queue:
      sender, signal, receivers = signal_queue.popleft()

      self.emitted[signal] += len(receivers)

      for receiver in receivers:
        if verbose:
          print("{} -{}-> {}".format(sender, signal.name, receiver))

        try:
          result = self.modules[receiver].handle(sender, signal)
          if result is not None:
            signal_queue.append(result)
        except KeyError:
          pass

    self.presses += 1

  def find_cycle(self, max_length = None):
    if self.cycle is not None:
      return self.cycle[0]

    self.reset()

    while max_length is None or self.presses < max_length:
      self.press_button(verbose = False)

      if self.is_initial:
        break

      if self.presses == max_length:
        return False

    self.cycle = (self.presses, *self.emitted)

    self.reset()

    return self.cycle[0]

  def hammer(self, presses = 1000):
    if self.find_cycle(max_length = presses):
      period, *emissions = self.cycle

      self.reset()

      for _ in range(presses % period):
        self.press_button(verbose = False)

      self.emitted = [ from_remainder + (presses // period) * from_cycle for from_remainder, from_cycle in zip(self.emitted, emissions) ]

    return reduce(mul, self.emitted)

  def __str__(self):
    return "".join(str(self.modules[name]) for name in sorted(self.modules))

  def analyse(self):
    driver = [ name for name, module in self.all_modules.items() if "rx" in module.outputs ][0]
    seeds = [ name for name, module in self.all_modules.items() if driver in module.outputs ]

    subsets = [ { name for name, module in self.all_modules.items() if seed in module.outputs } for seed in seeds ]

    for subset in subsets:
      while True:
        additions = { name for name, module in self.all_modules.items() if not name in subset and any(target in module.outputs for target in subset) }

        if not additions:
          break

        subset.update(additions)

      self.cycle = None

      self.modules = { name: self.all_modules[name] for name in subset }

      self.reset()

      self.subsets.append((self.find_cycle(), subset))

def read_input():
  machines = Machines()

  for line in fileinput.input():
    name, receivers = line.strip().split(" -> ")

    try:
      module_type = MODULES[name[0]]
      name = name[1:]
    except KeyError:
      module_type = Broadcaster

    module = module_type(name)

    for receiver in receivers.split(", "):
      module.connect_to(receiver)

    machines.add_module(module)

  machines.connect_inputs()

  return machines

def main():
  machines = read_input()

  # part 1
  print(machines.hammer(1000))

  # part 2
  machines.reset()
  machines.analyse()

  print(reduce(lcm, (subset[0] for subset in machines.subsets)))

if __name__ == "__main__":
  main()
