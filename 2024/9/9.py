#!/usr/bin/python3

import fileinput
from more_itertools import chunked

EMPTY = "."

class Map:
    def __init__(self, line):
        self._memory = []
        self.initial_files = [] # map fileno to size and initial position
        self.gaps = [] # list of gap sizes and positions
        for fileno, sizes in enumerate(chunked(line.strip(), 2)):
            filesize = int(sizes[0])
            self.initial_files.append((filesize, len(self._memory)))
            self._memory.extend([ fileno ] * filesize)
            self.lastfileblock = len(self._memory) - 1
            try:
                gapsize = int(sizes[1])
                self.gaps.append((gapsize, len(self._memory)))
                self._memory.extend([ EMPTY ] * gapsize)
            except IndexError:
                pass
        self.firstempty = self._memory.index(EMPTY)
    
    def __str__(self):
        return "".join(map(str, self._memory))

    def has_gap(self):
        return self.firstempty < self.lastfileblock

    def compact_blocks(self):
        while self.has_gap():
            self._memory[self.firstempty] = self._memory[self.lastfileblock]
            self._memory[self.lastfileblock] = EMPTY
            self.firstempty = self._memory.index(EMPTY)
            while self._memory[self.lastfileblock] == EMPTY:
                self.lastfileblock -= 1

    def find_and_fill_gap(self, needed_size, max_position):
        for index, (size, position) in enumerate(self.gaps):
            if position >= max_position:
                return 0
            if size >= needed_size:
                self.gaps[index] = (size - needed_size, position + needed_size)
                return position
        return 0

    def compact_files(self):
        for fileno, (size, position) in reversed(list(enumerate(self.initial_files))):
            if destination := self.find_and_fill_gap(size, position):
                for offset in range(size):
                    self._memory[destination + offset] = fileno
                    self._memory[position + offset] = EMPTY

    def checksum(self):
      return sum(position * (0 if filenumber == EMPTY else filenumber) for position, filenumber in enumerate(self._memory))
    
def main():
    line = fileinput.input().readline()
    fileinput.close()

    # part 1
    diskmap = Map(line)
    diskmap.compact_blocks()
    print(diskmap.checksum())

    # part 2
    diskmap = Map(line)
    diskmap.compact_files()
    print(diskmap.checksum())

if __name__ == "__main__":
    main()
