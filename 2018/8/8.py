#!/usr/bin/python3

import fileinput

class Node:
  def __init__(self,parent,n_children,n_metadata):
    self.parent = parent
    self.n_children = n_children
    self.n_metadata = n_metadata
    self.children = []
    self.metadata = []

  def value(self):
    if self.n_children == 0:
      return sum(self.metadata)
    else:
      value = 0
      for index in self.metadata:
        if index - 1 in range(len(self.children)):
          value += self.children[index-1].value()
      return value

  def __repr__(self):
    return "N({}): {}/{}, {}".format(self.parent,self.n_children,self.n_metadata,self.metadata)

def read_nodes(tree_data,parent=None,position=0):
#  print(position*" ",position,tree_data)
  n_children, n_metadata = tree_data[:2]
  new_nodes = {position: Node(parent,n_children,n_metadata)}
#  print(position*" ",position,new_nodes)
  index = position+2
  for n in range(n_children):
    children,index = read_nodes(tree_data[index-position:],position,index)
    new_nodes.update(children)
    new_nodes[position].children.extend(c for c in children.values() if c.parent == position)
#    print(position*" ",position,new_nodes)
  new_nodes[position].metadata = tree_data[index-position:index-position+tree_data[1]]
  return new_nodes,index+n_metadata

def main():
  tree_data = list(map(int,fileinput.input().readline().split()))
  nodes,_ = read_nodes(tree_data)
  print(sum(sum(node.metadata) for node in nodes.values()))
  print(nodes[0].value())

if __name__ == "__main__":
  main()
