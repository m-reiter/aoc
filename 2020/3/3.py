#!/usr/bin/python3

import fileinput

class Vector:
  def __init__(self,x,y):
    self.x = x
    self.y = y
  def __add__(self,other):
    return Vector((self.x+other.x) % self.wrap, self.y+other.y)
  def __repr__(self):
    return "[{},{}]".format(self.x,self.y)

def count_trees(map,start,course):

  pos = start
  trees = 0

  while pos.y < len(map):
    if map[pos.y][pos.x] == "#":
      trees +=1
    pos = pos+course

  return trees

def main():
  
  map = [ line.strip() for line in fileinput.input() ]

  Vector.wrap = len(map[0])

  start = Vector(0,0)
  course = Vector(3,1)

  sol1 = count_trees(map,start,course)

  # part 2

  courses = [
    Vector(1,1),
    Vector(3,1),
    Vector(5,1),
    Vector(7,1),
    Vector(1,2)
  ]

  sol2 = 1

  for course in courses:
    sol2 *= count_trees(map,start,course)

  print(sol1)
  print(sol2)

if __name__ == "__main__":
  main()
