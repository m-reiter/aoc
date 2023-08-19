#!/usr/bin/python3

import fileinput
import re

ARGS = re.compile("(\d+)x(\d+)")

def decompress(string):
  decompressed = ""
  tokens = list(string)
  while tokens:
    token = tokens.pop(0)
    if token == "(":
      end = tokens.index(")")
      length,times = map(int,ARGS.match("".join(tokens[:end])).groups())
      expanded = "".join(tokens[end+1:end+1+length])*times
      decompressed += expanded
      tokens = tokens[end+1+length:]
    else:
      decompressed += token
  return decompressed

def get_length_v2(string):
  decompressed_length = 0
  while "(" in string:
    pos = string.index("(")
    decompressed_length += pos
    string = string[pos+1:]
    end = string.index(")")
    length,times = map(int,ARGS.match(string).groups())
    expanded = string[end+1:end+1+length]
    decompressed_length += times*get_length_v2(expanded)
    string = string[end+1+length:]
  decompressed_length += len(string)
  return decompressed_length

def main():
  input = [line.strip() for line in fileinput.input()]
  for line in input:
    print(len(decompress(line)))
    print(get_length_v2(line))

if __name__ == "__main__":
  main()
