#!/usr/bin/python3

import hashlib
import re

SALT="yjdafjpo"
#SALT="abc"
TRIPLET = re.compile("(.)\\1\\1")

def stretch_hash(h):
  for _ in range(2016):
    h = hashlib.md5(h.encode()).hexdigest()
  return h

def generate_keys(n,stretch=False):
  hashes = [ hashlib.md5((SALT+str(i)).encode()).hexdigest() for i in range(1000) ]
  if stretch:
    hashes = [ stretch_hash(h) for h in hashes ]
  keys = []
  position = 0
  while len(keys) < n:
    #print(position,hashes[position])
    h = hashlib.md5((SALT+str(position+1000)).encode()).hexdigest()
    if stretch:
      h = stretch_hash(h)
    hashes.append(h)
    m = TRIPLET.search(hashes[position])
    if m:
      five = m.group()[0]*5
      if any(five in h for h in hashes[position+1:position+1001]):
        keys.append(hashes[position])
    position += 1
  return position-1

def main():
  print(generate_keys(64))
  print(generate_keys(64,stretch=True))

if __name__ == "__main__":
  main()
