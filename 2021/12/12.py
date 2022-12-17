#!/usr/bin/python3

import fileinput
from collections import defaultdict

class Cave:
  
  def __init__(self):
    self.name = None
    self.links = []

  def link_to(self,other):
    self.links.append(other)
    other.links.append(self)

  def __repr__(self):
    return "cave '{}'->{}".format(self.name,[link.name for link in self.links])

def read_input():
  system = defaultdict(Cave)

  for line in fileinput.input():
    start,end = line.strip().split("-")
    system[start].link_to(system[end])
    for name in start,end:
      system[name].name = name

  return system

def find_paths(start,path_so_far=[],d=0,twice=False):
#  print("    "*d,"searching from {} ({})".format(start.name,path_so_far))
  path_so_far = path_so_far+[start.name]
  if start.name == "end":
    return [path_so_far]
  paths_from_here = []
  for cave in start.links:
    if cave.name.isupper() or not cave.name in path_so_far:
#      print("    "*d,cave.name)
      paths_from_here += find_paths(cave,path_so_far,d+1,twice=twice)
    elif cave.name != "start" and not twice:
#      print("    "*d,cave.name)
      paths_from_here += find_paths(cave,path_so_far,d+1,twice=True)
#  print("    "*d,paths_from_here)
  return paths_from_here

def main():
  system = read_input()
  paths = find_paths(system["start"],twice=True)

  for path in paths:
    print(",".join(path))

  print(len(paths))

  paths2 = find_paths(system["start"],twice=False)
  print(len(paths2))

if __name__ == "__main__":
  main()
