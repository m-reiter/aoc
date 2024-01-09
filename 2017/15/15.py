#!/usr/bin/python3

DIVISOR = 2147483647
FACTORS = 16807, 48271

STARTING_VALUES = 65, 8921
STARTING_VALUES = 703, 516
VALIDATORS = (lambda x: x % 4 == 0, lambda x: x % 8 == 0)

class Generator():

  def __init__(self,starting_value, factor, validate = lambda x: True):
    self.starting_value = starting_value
    self.factor = factor
    self.values = []
    self.validate = validate

  def generate(self):
    try:
      candidate = self.values[-1]
    except IndexError:
      candidate = self.starting_value
    while True:
      candidate = candidate * self.factor % DIVISOR
      if self.validate(candidate):
        break
    self.values.append(candidate)

def part1():
  generators = tuple(Generator(starting_value, factor) for starting_value, factor in zip(STARTING_VALUES, FACTORS))
  print("--Gen. A--  --Gen. B--")
  for _ in range(5):
    for generator in generators:
      generator.generate()
    print("{:10d}  {:10d}".format(generators[0].values[-1],generators[1].values[-1]))
  print(sum(a & 2**16-1 == b & 2**16-1 for a,b in zip(generators[0].values,generators[1].values)))
  print("[",end="",flush=True)
  for _ in range(100000-5):
    for generator in generators:
      generator.generate()
  print(".",end="",flush=True)
  for _ in range(398):
    for _ in range(100000):
      for generator in generators:
        generator.generate()
    print(".",end="",flush=True)
  for _ in range(100000-5):
    for generator in generators:
      generator.generate()
  print("]")
  for _ in range(5):
    for generator in generators:
      generator.generate()
    print("{:10d}  {:10d}".format(generators[0].values[-1],generators[1].values[-1]))
  print(sum(a & 2**16-1 == b & 2**16-1 for a,b in zip(generators[0].values,generators[1].values)))

def part2():
  generators = tuple(Generator(starting_value, factor, validate) for starting_value, factor, validate in zip(STARTING_VALUES, FACTORS, VALIDATORS))
  print("--Gen. A--  --Gen. B--")
  for _ in range(5):
    for generator in generators:
      generator.generate()
    print("{:10d}  {:10d}".format(generators[0].values[-1],generators[1].values[-1]))
  print(sum(a & 2**16-1 == b & 2**16-1 for a,b in zip(generators[0].values,generators[1].values)))
  print("[",end="",flush=True)
  for _ in range(100000-5):
    for generator in generators:
      generator.generate()
  print(".",end="",flush=True)
  for _ in range(48):
    for _ in range(100000):
      for generator in generators:
        generator.generate()
    print(".",end="",flush=True)
  for _ in range(100000-5):
    for generator in generators:
      generator.generate()
  print("]")
  for _ in range(5):
    for generator in generators:
      generator.generate()
    print("{:10d}  {:10d}".format(generators[0].values[-1],generators[1].values[-1]))
  print(sum(a & 2**16-1 == b & 2**16-1 for a,b in zip(generators[0].values,generators[1].values)))

def main():
  #part1()
  part2()

if __name__ == "__main__":
  main()
