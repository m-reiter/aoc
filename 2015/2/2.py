#!/usr/bin/python3

import fileinput
from itertools import combinations
from functools import reduce
from operator import mul

def main():
  dimensions = [ tuple(map(int,line.split("x"))) for line in fileinput.input() ]
  areas = [ tuple(a*b for a,b in combinations(sides,2)) for sides in dimensions ]
  totals = [ 2*sum(areas)+min(areas) for areas in areas ]
  print(sum(totals))

  volumes = [ reduce(mul,sides) for sides in dimensions ]
  circumferences = [ 2*sum(sorted(sides)[:2]) for sides in dimensions ]
  lengths = [ v+c for v,c in zip(volumes,circumferences) ]
  print(sum(lengths))

if __name__ == "__main__":
  main()
