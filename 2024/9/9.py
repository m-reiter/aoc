#!/usr/bin/python3

import fileinput
from more_itertools import chunked

EMPTY = "."

class Map:
    def __init__(self, line):
        self._memory = []
        self.initial_files = {} # dict to map fileno to size and initial position
        for fileno, sizes in enumerate(chunked(line.strip(), 2)):
            filesize = int(sizes[0])
            self._memory.extend([ fileno ] * int(sizes[0]))
            self.lastfileblock = len(self._memory) - 1
            try:
                self._memory.extend([ EMPTY ] * int(sizes[1]))
            except IndexError:
                pass
        self.firstempty = self._memory.index(EMPTY)
    
    def __str__(self):
        return "".join(map(str, self._memory))

    def has_gap(self):
        return self.firstempty < self.lastfileblock

    def compact(self):
        while self.has_gap():
            self._memory[self.firstempty] = self._memory[self.lastfileblock]
            self._memory[self.lastfileblock] = EMPTY
            self.firstempty = self._memory.index(EMPTY)
            while self._memory[self.lastfileblock] == EMPTY:
                self.lastfileblock -= 1
#            print(self)

    def checksum(self):
      return sum(position * filenumber for position, filenumber in enumerate(self._memory[:self.firstempty]))
    
def main():
    line = fileinput.input().readline()
    fileinput.close()
    
    diskmap = Map(line)

    # part 1
    diskmap.compact()
    print(diskmap.checksum())

if __name__ == "__main__":
    main()
