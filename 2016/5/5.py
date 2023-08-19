#!/usr/bin/python3

import hashlib

DOOR="abc"

def part1(pw,hex_hash):
  if pw is None:
    pw = ""
  pw += hex_hash[5]
  print(pw)
  return pw

def part2(pw,hex_hash):
  if pw is None:
    pw = dict()
  position = int(hex_hash[5],base=16)
  if position < 8 and position not in pw:
    pw[position] = hex_hash[6]
    print("".join(pw[i] if i in pw else "_" for i in range(8)))
  return pw

def calculate_password(door=DOOR,fill_pw=part1):
  i = 0
  pw = None
  while True:
    hex_hash = hashlib.md5((door+str(i)).encode()).hexdigest()
    if hex_hash.startswith("00000"):
      pw = fill_pw(pw,hex_hash)
      if len(pw) == 8:
        break
    i += 1
  return pw

def main():
  #print(calculate_password("ugkcyxxp"))
  pw = calculate_password("ugkcyxxp",fill_pw=part2)
  print("".join(pw[i] for i in range(8)))

if __name__ == "__main__":
  main()
