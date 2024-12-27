#!/usr/bin/python3

import fileinput
from collections import defaultdict

from P import P

START = "S"
END = "E"
WALL = "#"

class RaceTrack:
  def __init__(self, trackmap):
    self.track = set()
    self.course = {}
    self.shortcuts = defaultdict(list)
    self.extended_shortcuts = defaultdict(set)
    for y, line in enumerate(trackmap):
      for x, char in enumerate(line.strip()):
        if char == WALL:
          continue
        if char == START:
          self.start = P(x,y)
        if char == END:
          self.end = P(x,y)
        self.track.add(P(x,y))

  def find_course(self):
    position = self.start
    length = 0
    while position != self.end:
      self.course[position] = length
      for neighbor in position.get_neighbors(diagonals = False):
        if neighbor not in self.course and neighbor in self.track:
          position = neighbor
          length += 1
          break
    self.course[self.end] = length

  def find_shortcuts(self):
    for start in self.course:
      for direction in P.offsets(diagonals = False):
        end = start + 2 * direction
        if end in self.course and (saving := self.course[end] - self.course[start] - 2) > 0:
          self.shortcuts[saving].append((start, end))

  def find_extended_shortcuts(self):
    for start in self.course:
      for end in self.course:
        distance = sum(map(abs, end - start))
        saving = self.course[end] - self.course[start] - distance
        if distance <= 20 and saving > 0:
          self.extended_shortcuts[saving].add((start, end))

def main():
  racetrack = RaceTrack(fileinput.input())
  racetrack.find_course()
  racetrack.find_shortcuts()
  racetrack.find_extended_shortcuts()

  # part 1
  print(sum(len(v) for k,v in racetrack.shortcuts.items() if k >= 100))

  # part 2
  print(sum(len(v) for k,v in racetrack.extended_shortcuts.items() if k >= 100))

if __name__ == "__main__":
  main()
