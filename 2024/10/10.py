import fileinput
from collections import defaultdict

from P import P

class Map:
    def __init__(self, inputdata):
        self.tiers = defaultdict(list)
        self.reachable = defaultdict(set)
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
                        else:
                            self.reachable[n] |= self.reachable[p]
            tier -= 1
                
def main():
    m = Map(fileinput.input())
    
    # part 1
    m.find_trails()
    print(sum(len(m.reachable[p]) for p in m.tiers[0]))

if __name__ == "__main__":
    main()