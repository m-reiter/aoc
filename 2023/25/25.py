#!/usr/bin/python3

import fileinput
import networkx as nx

from itertools import combinations

def read_input():
  diagram = nx.Graph()

  for line in fileinput.input():
    part, connections = line.strip().split(": ")
    
    for connection in connections.split():
      diagram.add_edge(part, connection)

  return diagram

def part1(diagram):
  d = diagram.copy()

  d.remove_edges_from(nx.minimum_edge_cut(d))

  groups = list(nx.connected_components(d))

  assert len(groups) == 2

  a, b = map(len, groups)

  return a * b

def main():
  diagram = read_input()

  print(part1(diagram))

if __name__ == "__main__":
  main()
