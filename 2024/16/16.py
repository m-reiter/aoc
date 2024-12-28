#!/usr/bin/python3

import fileinput
from collections import defaultdict, deque

from P import P

START = "S"
END = "E"
WALL = "#"
EMPTY = "."

NORTH = P( 0, -1)
SOUTH = P( 0,  1)
EAST  = P( 1,  0)
WEST  = P(-1,  0)

TURNS = {
  NORTH: (EAST, WEST),
  SOUTH: (EAST, WEST),
  EAST : (NORTH, SOUTH),
  WEST : (NORTH, SOUTH)
}

class ReindeerMaze(dict):
  def __init__(self, lines):
    for y, line in enumerate(lines):
      for x, char in enumerate(line.strip()):
        self[P(x,y)] = char
        if char == START:
          self.start = P(x,y)
        if char == END:
          self.end = P(x,y)
    self.best_scores = defaultdict(int)
    self.best_score = None
    self.best_paths = defaultdict(list)
    self.best_seats = { self.start, self.end }

  def find_paths(self):
    self.best_scores[(self.start, EAST)] = 0
    self.best_paths[(self.start, EAST)].append([])
    to_check = deque([ (self.start, EAST, 0) ]) # tuples are (position, facing, score)

    while to_check:
      position, facing, score = to_check.popleft()
      for neighbor, new_facing, new_score in [ (position + facing, facing, score + 1) ] + [ (position, turn, score + 1000) for turn in TURNS[facing] ]:
        is_new = (neighbor, new_facing) not in self.best_scores
        if not is_new:
          previous_best = self.best_scores[(neighbor, new_facing)]
        if self[neighbor] != WALL and (is_new or new_score <= previous_best):
          new_paths = [ previous + [ position ] for previous in self.best_paths[(position, facing)] ]
          if is_new or new_score < previous_best:
            self.best_scores[(neighbor, new_facing)] = new_score
            self.best_paths[(neighbor, new_facing)] = new_paths
            if neighbor != self.end:
              to_check.append((neighbor, new_facing, new_score))
          else:
            self.best_paths[(neighbor, new_facing)].extend(new_paths)

    self.best_score = min(score for (position, facing), score in self.best_scores.items() if position == self.end)
    for situation in [ (position, facing) for (position, facing), score in self.best_scores.items() if position == self.end and score == self.best_score ]:
      for path in self.best_paths[situation]:
        self.best_seats.update(path)

def main():
  maze = ReindeerMaze(fileinput.input())

  # part 1
  maze.find_paths()
  print(maze.best_score)

  # part 2
  print(len(maze.best_seats))

if __name__ == "__main__":
  main()
