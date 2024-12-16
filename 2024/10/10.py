#!/usr/bin/python3

import fileinput
from collections import defaultdict

from P import P

class Map:
    def __init__(self, inputdata):
        self.tiers = defaultdict(list)
        self.reachable = defaultdict(set)
        self.distinct_trails = defaultdict(list)
        for y, line in enumerate(inputdata):
            for x, char in enumerate(line.strip()):
                self.tiers[int(char)].append(P(x, y))
        self.borders = P(x, y)
    
    def find_trails(self):
        tier = 9
        while tier > 0:
            for p in self.tiers[tier]:
                for n in p.get_neighbors(diagonals = False, borders = self.borders):
                    if n in self.tiers[tier - 1]:
                        if tier == 9:
                            self.reachable[n].add(p)
                            self.distinct_trails[n].append([ p ])
                        else:
                            self.reachable[n] |= self.reachable[p]
                            self.distinct_trails[n].extend([[ p ] + trail for trail in self.distinct_trails[p]])
            tier -= 1
#            for k in sorted(self.distinct_trails.keys()):
#                if k in self.tiers[tier]:
#                    print(k, self.distinct_trails[k])
                
def main():
    m = Map(fileinput.input())
    m.find_trails()
    
    # part 1
    print(sum(len(m.reachable[p]) for p in m.tiers[0]))

    # part 2
    print(sum(len(m.distinct_trails[p]) for p in m.tiers[0]))

if __name__ == "__main__":
    main()
