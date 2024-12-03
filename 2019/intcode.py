class Computer:

  def add(self, x):
      pass

  def multiply(self, x):
      pass

  def halt(self):
      pass

  OPCODES = { # map Opcode to function and number of args
      1: (add, 3),
      2: (multiply, 3),
      99: (halt, 0)
  }
