#!/usr/bin/python3

import fileinput
import re
from collections import defaultdict

from P import P

PATTERN = re.compile("Sensor at x=(-?\d+), y=(-?\d+): closest beacon is at x=(-?\d+), y=(-?\d+)")

class Range():
  
  def __init__(self):
    self.ranges = []

  def add(self,newrange):
    self.ranges.append(newrange)

  def consolidate(self):
    start = None
    ranges = []
    for interval in sorted(self.ranges):
      if start is None:
        start,end = interval
      else:
        if interval[0]-end <= 1:
          end = interval[1]
        else:
          ranges.append((start,end))
          start,end = interval
    ranges.append((start,end))
    self.ranges = ranges

  def count(self):
    print("count: ",self.ranges)
    return sum(x[1]-x[0]+1 for x in self.ranges)

  def has_gap(self):
    return len(self.ranges) > 1

def manhattan(p1,p2):
  return abs(p1.x-p2.x)+abs(p1.y-p2.y)

def dimensions(cave):
  xmin = min(p.x for p in cave.keys())
  xmax = max(p.x for p in cave.keys())
  ymin = min(p.y for p in cave.keys())
  ymax = max(p.y for p in cave.keys())
  return xmin,xmax,ymin,ymax

def read_data():
  cave = defaultdict(Range)
  sensors = []
  beacons = set()
  for x_sensor,y_sensor,x_beacon,y_beacon in [list(map(int,PATTERN.match(line).groups())) for line in fileinput.input()]:
    sensor = P(x_sensor,y_sensor)
    beacon = P(x_beacon,y_beacon)
    distance = manhattan(sensor,beacon)
    #print("*",sensor,beacon,distance)
    for y in range(-distance,distance+1):
    #  print("***",sensor.y+y,cave[sensor.y+y])
      cave[sensor.y+y].add((sensor.x-((distance-abs(y))),sensor.x+(distance-abs(y))))
    #  print("***",sensor.y+y,cave[sensor.y+y])
    sensors.append(sensor)
    beacons.add(beacon)
  for row in cave.values():
    row.consolidate()
  return cave,sensors,beacons

def main():
  cave,sensors,beacons = read_data()
  #print(beacons)

  # part 1
  if len(sensors) == 14: # sample data
    row = 10
  else:
    row = 2000000
  print(cave[row].count()-len([beacon for beacon in beacons if beacon.y == row]))
  
  # part 2
  print("part 2")
  if len(sensors) == 14: # sample data
    maxcoord = 20
  else:
    maxcoord = 4000000
  for y in range(0,maxcoord+1):
    if cave[y].has_gap():
      print(cave[y].ranges)
      x = cave[y].ranges[0][1]+1
      print(x,y)
      print(x*4000000+y)
      break
  return

if __name__ == "__main__":
  main()
