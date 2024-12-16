#!/usr/bin/python3

import fileinput
from collections import Counter, defaultdict
from functools import cache, lru_cache

#@lru_cache(maxsize = 1)
@cache
def blink(stone):
    if stone == 0:
        next_gen = [ 1 ]
    elif (l := len(s := str(stone))) % 2 == 0:
        next_gen = list(map(int, [s[:l // 2], s[l // 2:]]))
    else:
        next_gen = [ stone * 2024 ]
    return next_gen

def evolve(stones, generations):
    #return sum(([ blink_n_times(stone, generations) ] * n for stone, n in Counter(stones)), [])
    if not isinstance(stones, dict):
        stones = Counter(stones)
    for _ in range(generations):
        steps = [ blink(stone) for stone in stones ]
        next_gen = defaultdict(int)
        for result, n in zip(steps, stones.values()):
            for stone in result:
                next_gen[stone] += n
        stones = next_gen
    return stones

def main():
    line = fileinput.input().readline()
    fileinput.close()

    stones = list(map(int, line.strip().split()))

    # part 1
    stones = evolve(stones, 25)
    print(sum(stones.values()))

    # part 2
    stones = evolve(stones, 50)
    print(sum(stones.values()))

if __name__ == "__main__":
    main()
