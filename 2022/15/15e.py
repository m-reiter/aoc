#!/usr/bin/python3

import fileinput
import re
from collections import defaultdict
from itertools import dropwhile

from P import P

PATTERN = re.compile("Sensor at x=(-?\d+), y=(-?\d+): closest beacon is at x=(-?\d+), y=(-?\d+)")

class Range:
  
  def __init__(self,limit = None):
    self.ranges = []
    self.limit = limit
    self.is_full = False

  def __repr__(self):
    return str(self.ranges)

  def add(self,newrange):
    self.ranges.append(newrange)

  def consolidate(self):
    #print("* consolidating {} ranges".format(len(self.ranges)))
    start = None
    ranges = []
    for interval in sorted(self.ranges):
      if start is None:
        start,end = interval
      else:
        if interval[0]-end <= 1:
          end = max(interval[1],end)
        else:
          ranges.append((start,end))
          start,end = interval
    ranges.append((start,end))
    self.ranges = ranges

  def truncate(self,limit):
    self.limit = limit
    ranges = dropwhile(lambda x: x[1] < 0, self.ranges)
    start,end = next(ranges)
    new_ranges = [(max(start,0),min(end,limit))]
    for start,end in ranges:
      if start > limit:
        break
      new_ranges.append((start,min(end,limit)))
      if end >= limit:
        break
    self.ranges = new_ranges

  def count(self):
    return sum(x[1]-x[0]+1 for x in self.ranges)

  def has_gap(self):
    gap = len(self.ranges) > 1
    if self.limit is not None:
      gap = gap or self.ranges[0][0] > 0 or self.ranges[-1][1] < self.limit
    return gap

def manhattan(p1,p2):
  return abs(p1.x-p2.x)+abs(p1.y-p2.y)

def read_data():
  cave = defaultdict(lambda : Range())
  beacons = defaultdict(set)
  for x_sensor,y_sensor,x_beacon,y_beacon in [list(map(int,PATTERN.match(line).groups())) for line in fileinput.input()]:
    sensor = P(x_sensor,y_sensor)
    beacon = P(x_beacon,y_beacon)
    distance = manhattan(sensor,beacon)
    print("* processing sensor ",sensor,beacon,distance)
    for y in range(-distance,distance+1):
    #  print("***",sensor.y+y,cave[sensor.y+y])
      cave[sensor.y+y].add((sensor.x-((distance-abs(y))),sensor.x+(distance-abs(y))))
    #  print("***",sensor.y+y,cave[sensor.y+y])
    beacons[beacon.y].add(beacon)
    #print(cave)
  #for row in cave.values():
  #  row.consolidate()
  return cave,beacons

def main():
  cave,beacons = read_data()
  sample_data = sum(len(x) for x in beacons.values()) == 6

  # part 1
  if sample_data: # sample data
    row = 10
  else:
    row = 2000000
  cave[row].consolidate()
  print(cave[row].count()-len(beacons[row]))
  
  # part 2
  print("part 2")
  if sample_data:
    maxcoord = 20
  else:
    maxcoord = 4000000
  for y in range(0,maxcoord+1):
    if y % 1000 == 0:
      print(y)
    cave[y].consolidate()
    cave[y].truncate(maxcoord)
    if cave[y].has_gap():
      print(cave[y].ranges)
      x = cave[y].ranges[0][1]+1
      print(x,y)
      print(x*4000000+y)
      break
  print(cave[11].has_gap())

if __name__ == "__main__":
  main()
