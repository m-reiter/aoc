#!/usr/bin/python3

import fileinput
from pathlib import Path
from collections import defaultdict

TOTAL = 70000000
NEEDED = 30000000

class Directory():
  def __init__(self,path,parent=None):
    self.path = path
    self.parent = parent if parent else self
    self.contents = {}

  @property
  def size(self):
    return sum(object.size for object in self.contents.values())

  def __repr__(self):
    return "dir({})".format(self.path)

class File():
  def __init__(self,size):
    self.size = int(size)

  def __repr__(self):
    return "file({})".format(self.size)

def read_input():
  root = Directory(Path("/"))
  cwd = root
  alldirs = [root]

  for line in fileinput.input():
    tokens = line.strip().split()
    if tokens[0] == "$":
      cmd,*args = tokens[1:]
      if cmd == "cd":
        name = args[0]
        if name == "/":
          cwd = root
        elif name == "..":
          cwd = cwd.parent
        else:
          cwd = cwd.contents[name]
      else:
        # can only be ls, ignore
        pass
    else:
      # ls output
      size_or_type,name = tokens
      if size_or_type == "dir":
        if name not in cwd.contents:
          newdir = cwd.contents[name] = Directory(cwd.path / name,cwd)
          alldirs.append(newdir)
      else:
        cwd.contents[name] = File(size_or_type)

  return root,alldirs

def part1(dirs):
  return sum(dir.size for dir in dirs if dir.size <= 100000)
  
def part2(root,dirs):
  free = TOTAL - root.size
  return min(dir.size for dir in dirs if dir.size+free >= NEEDED)
  
def main():
  root,alldirs = read_input()

  print(part1(alldirs))
  print(part2(root,alldirs))

if __name__ == "__main__":
  main()
