#!/usr/bin/python3

import fileinput

def get_group(node,connections):
  group = set()
  to_check = [ node ]
  while to_check:
    for node in connections[to_check.pop(0)]:
      if node not in group:
        group.add(node)
        to_check.append(node)
  return group
  
def main():
  report = [ line.strip() for line in fileinput.input() ]

  connections = {}
  for line in report:
    node,destinations = line.split(" <-> ")
    destinations = destinations.split(", ")
    connections[node] = destinations

  # part1
  group0 = get_group("0",connections)
  print(len(group0))

  # part2
  number_of_groups = 1
  accounted = group0
  while set(connections.keys()) != accounted:
    number_of_groups += 1
    node = (set(connections.keys()) - accounted).pop()
    accounted |= get_group(node,connections)
  print(number_of_groups)

if __name__ == "__main__":
  main()
