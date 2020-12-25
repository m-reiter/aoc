#!/usr/bin/python3

# sample input

PUBLIC_KEYS = [5764801, 17807724]

# real input

PUBLIC_KEYS = [8458505, 16050997]

class Encryption:

  def __init__(self, subject):

    self.value = 1
    self.subject = subject

  def next(self):

    self.value = (self.value * self.subject) % 20201227

class CodeBreaker(Encryption):

  def __init__(self, public_keys):

    super().__init__(7)
    self.public_keys = public_keys
    self.key_to_loop = {}

  def solve(self):

    loop = 0
    
    while not all(key in self.key_to_loop for key in self.public_keys):

      for loop in range(loop, loop + 1000):

        self.key_to_loop[self.value] = loop
        self.next()

      loop += 1

    return [self.key_to_loop[key] for key in self.public_keys]

class Encrypter:

  def __init__(self, loop):

    self.loop = loop

  def encrypt(self, subject):

    encrypter = Encryption(subject)

    for i in range(self.loop):

      encrypter.next()

    return encrypter.value


def main():
  
  loops = CodeBreaker(PUBLIC_KEYS).solve()

  print(loops)

  encryption_keys = [Encrypter(loop).encrypt(subject) for loop, subject in zip(loops, reversed(PUBLIC_KEYS))]

  print(encryption_keys)

if __name__ == "__main__":
  main()
