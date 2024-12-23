#!/usr/bin/python3

import fileinput
import networkx as nx

def get_input():
  network = nx.Graph()
  network.add_edges_from(line.strip().split("-") for line in fileinput.input())
  return network

def main():
  pass
  network = get_input()

  # part 1
  print(len([c for c in nx.enumerate_all_cliques(network) if len(c) == 3 and any(n.startswith("t") for n in c)]))

  # part 2
  print(",".join(sorted(max([c for c in nx.find_cliques(network)], key = len))))

if __name__ == "__main__":
  main()
