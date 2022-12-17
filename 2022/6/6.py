#!/usr/bin/python3

import fileinput

def find_markers(signal,length):
  return [i for i in range(length,len(signal)) if len(set(signal[i-length:i])) == length]

def main():
  signal = fileinput.input().readline().strip()

  packets = find_markers(signal,4)
  print(packets[0])

  messages = find_markers(signal,14)
  print(messages[0])

if __name__ == "__main__":
  main()
