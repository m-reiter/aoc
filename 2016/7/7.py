#!/usr/bin/python3

import fileinput
import re
from more_itertools import windowed,flatten

OUTER = re.compile("(?:\A|])([^\[]*)")
INNER = re.compile("\[(.*?)\]")

def read_data():
  return list(map(str.strip,fileinput.input()))

def is_abba(string):
  assert len(string) == 4
  return len(set(string)) == 2 and string == string[::-1]

def has_abba(string):
  return any(is_abba(x) for x in windowed(string,4))

def supports_tls(ipv7):
  outers = OUTER.findall(ipv7)
  inners = INNER.findall(ipv7)
  return any(map(has_abba,outers)) and not any(map(has_abba,inners))

def is_bab(string):
  assert len(string) == 3
  return len(set(string)) == 2 and string == string[::-1]

def get_babs(string):
  return [ substring for substring in windowed(string,3) if is_bab(substring) ]

def supports_ssl(ipv7):
  supernets = OUTER.findall(ipv7)
  hypernets = INNER.findall(ipv7)
  abas = { bab[1]+bab[0]+bab[1] for bab in flatten(map(get_babs,supernets)) }
  return any(any(aba in hyper for aba in abas) for hyper in hypernets)

def main():
  data = read_data()
  print(sum(map(supports_tls,data)))
  print(sum(map(supports_ssl,data)))

if __name__ == "__main__":
  main()
