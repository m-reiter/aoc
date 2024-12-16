#!/usr/bin/python3

import fileinput
from collections import defaultdict

def blink(stone):
    if stone == 0:
        return [ 1 ]
    if (l := len(s := str(stone))) % 2 == 0:
        return list(map(int, [s[:l // 2], s[l // 2:]]))
    return [ stone * 2024 ]

def blink_n_times(stones, n):
    for _ in range(n):
        print(_)
        new_stones = []
        for stone in stones:
            new_stones.extend(blink(stone))
        stones = new_stones
    return stones

def main():
    line = fileinput.input().readline()
    fileinput.close()

    stones = list(map(int, line.strip().split()))

    # part 1
    stones = blink_n_times(stones, 25)
    print(len(stones))

    # part 2
    stones = blink_n_times(stones, 50)
    print(len(stones))

if __name__ == "__main__":
    main()
