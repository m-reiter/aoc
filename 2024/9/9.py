import fileinput
from more_itertools import chunked

EMPTY = -1

class Map:
    def __init__(self, line):
        self._memory = []
        for fileno, sizes in enumerate(chunked(line.strip(), 2)):
            self._memory.expand([ fileno ] * sizes[0])
            self.lastfileblock = len(self._memory) - 1
            try:
                self._memory.expand([ EMPTY ] * sizes[1])
            except IndexError:
                pass
        self.firstempty = self._memory.index(EMPTY)
    
    def has_gap(self):
        return self.firstempty < self.lastfileblock
    
def main():
    line = fileinput.input().readline()
    fileinput.close()
    
    diskmap = Map(line)
    print(diskmap._memory)

if __name__ == "__main__":
    main()