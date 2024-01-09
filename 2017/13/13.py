#!/usr/bin/python3

import fileinput

def get_severity(scanners, start = 0):
  severity = 0
  for depth,scan_range in scanners.items():
    if (depth + start) % (2 * scan_range - 2) == 0:
      severity += depth * scan_range
  return severity

def is_unsafe(scanners, start = 0):
  for depth,scan_range in scanners.items():
    if (depth + start) % (2 * scan_range - 2) == 0:
      return True
  return False

def main():
  scanners = {}
  for line in fileinput.input():
    depth,scan_range = map(int,line.strip().split(": "))
    scanners[depth] = scan_range
  print(get_severity(scanners))

  delay = 1
  while is_unsafe(scanners,delay):
    delay += 1
  print(delay)

if __name__ == "__main__":
  main()
