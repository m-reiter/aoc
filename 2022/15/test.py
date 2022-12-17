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
    left = [x for x in self.ranges if x[1] < newrange[0]-1]
    right = [x for x in self.ranges if x[0] > newrange[1]+1]
    middle = self.ranges[len(left):len(self.ranges)-len(right)+1]
    if middle:
      newrange = (min(newrange[0],middle[0][0]),max(newrange[1],middle[-1][1]))
    self.ranges = left + [newrange] + right

  def count(self,minx=None,maxx=None):
    count = 0
    if minx is None:
      minx = self.ranges[0][0]
    if maxx is None:
      maxx = self.ranges[-1][1]
    for x in range(minx,maxx+1):
      if any(x in range(left,right+1) for left,right in self.ranges):
        count += 1
    return count

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
    if cave[y].count(0,maxcoord) != maxcoord+1:
      x = cave[y].ranges[0][1]+1
      print(x*4000000+y)
      break
  return

if __name__ == "__main__":
  main()
