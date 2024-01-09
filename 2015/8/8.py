#!/usr/bin/python3

import fileinput

def memory_length(string):
  string = string.strip('"')
  length = string.count(r'\\')
  string = string.replace(r'\\','')
  length += string.count(r'\"')
  string = string.replace(r'\"','')
  length += len(string) - 3 * string.count(r"\x")

  return length

def code_length(string):
#  string = string.strip('"')

#  return len(string) + 6 + string.count("\\") + string.count('"')
  string = string.replace("\\","\\\\")
  string = string.replace('"',r'\"')
  string = '"'+string+'"'
  return len(string)
  
def main():
  strings = [ line.strip() for line in fileinput.input() ]

  print(sum(map(len,strings)) - sum(map(memory_length,strings)))
  print(sum(map(code_length,strings)) - sum(map(len,strings)))
  
  for line in strings:
    print(line,len(line),code_length(line))

if __name__ == "__main__":
  main()
