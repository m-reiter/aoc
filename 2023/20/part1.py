#!/usr/bin/python3

import fileinput

from enum import IntEnum
from attr import attrs, attrib
from collections import deque
from functools import reduce
from operator import mul

class Signal(IntEnum):
  low = 0
  high = 1

  def __str__(self):
    return self.name

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

@attrs
class Rx(Module):
  fired = attrib(default = False)
  hits = attrib(default = 0)

  def handle(self, sender, signal):
    if signal == Signal.low:
      self.fired = True
      self.hits += 1

  def reset(self):
    self.hits = 0


MODULES = {
  "%": FlipFlop,
  "&": Conjunction
}

@attrs
class Machines:
  modules = attrib(factory = dict)
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

  def fires(self):
    rxs = [ m for m in self.modules.values() if isinstance(m, Rx) ]
    return "*** {}".format(" ".join("{}:{}".format(m.name, m.hits) for m in rxs))

  def connect_inputs(self):
    senders = list(self.modules.values())
    for sender in senders:
      for receiver in sender.outputs:
        if not receiver in self.modules:  
          #self.add_module(Module(receiver))
          self.add_module(Rx(receiver))

        self.modules[receiver].connect_from(sender.name)

  def press_button(self, verbose = True):
    signal_queue = deque([ ("button", Signal.low, [ "broadcaster" ]) ])

    while signal_queue:
      sender, signal, receivers = signal_queue.popleft()

      self.emitted[signal] += len(receivers)

      for receiver in receivers:
        if verbose:
          print("{} -{}-> {}".format(sender, str(signal), receiver))

        result = self.modules[receiver].handle(sender, signal)
        if result is not None:
          signal_queue.append(result)

    self.presses += 1

  def find_cycle(self, max_length = None):
    if self.cycle is not None:
      return True

    self.reset()

    while max_length is None or self.presses < max_length:
      self.press_button(verbose = False)

      if self.is_initial:
        break

      if self.presses == max_length:
        return False

    self.cycle = (self.presses, *self.emitted)

    self.reset()

    return True

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
  print(machines.hammer(10000))
  print(machines.cycle)

  # part 2
  machines.reset()
  machines.add_module(Rx("rx"))

  while True:
    print("{:4}".format(machines.presses), machines, machines.fires())
    machines.press_button(verbose = False)
    if not machines.presses % 100000:
      print("{:8}".format(machines.presses // 1000), end = "\r")

    if machines.modules["rx"].fired:
      break

  print("{:4}".format(machines.presses), machines, machines.fires(), machines.is_initial)
if __name__ == "__main__":
  main()
