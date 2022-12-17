#!/usr/bin/python3

import fileinput
import re
from collections import defaultdict

from P import P

EMPTY = '.'
SENSOR = 'S'
BEACON = 'B'
CLEAR = '#'

PATTERN = re.compile("Sensor at x=(-?\d+), y=(-?\d+): closest beacon is at x=(-?\d+), y=(-?\d+)")

def manhattan(p1,p2):
  return abs(p1.x-p2.x)+abs(p1.y-p2.y)

def dimensions(cave):
  xmin = min(p.x for p in cave.keys())
  xmax = max(p.x for p in cave.keys())
  ymin = min(p.y for p in cave.keys())
  ymax = max(p.y for p in cave.keys())
  return xmin,xmax,ymin,ymax

def show_cave(cave):
  xmin,xmax,ymin,ymax = dimensions(cave)
  for y in range(ymin,ymax+1):
    print("".join(cave[P(x,y)] for x in range(xmin,xmax+1)))

def clear_cave(cave,sensors):
  for sensor,distance in sensors:
    for y in range(-distance,distance+1):
      for x in range(-(distance-abs(y)),distance-abs(y)+1):
        #if cave[sensor+P(x,y)] == EMPTY:
          cave[sensor+P(x,y)] = CLEAR
  return cave

def read_data():
  cave = defaultdict(set)
  sensors = []
  beacons = []
  for x_sensor,y_sensor,x_beacon,y_beacon in [list(map(int,PATTERN.match(line).groups())) for line in fileinput.input()]:
    sensor = P(x_sensor,y_sensor)
    beacon = P(x_beacon,y_beacon)
    distance = manhattan(sensor,beacon)
    #print("*",sensor,beacon,distance)
    for y in range(-distance,distance+1):
    #  print("***",sensor.y+y,cave[sensor.y+y])
      cave[sensor.y+y] |= set(range(sensor.x-((distance-abs(y))),sensor.x+(distance-abs(y)+1)))
    #  print("***",sensor.y+y,cave[sensor.y+y])
    sensors.append(sensor)
    beacons.append(beacon)
  for beacon in beacons:
    try:
      cave[beacon.y].remove(beacon.x)
    except KeyError:
      pass
  return cave,sensors,beacons

def main():
  cave,sensors,beacons = read_data()
  #show_cave(cave)

  # part 1
  print(cave[10])
  print(len(cave[10]))
  return
  #clear_cave(cave,sensors)
  #show_cave(cave)
  #print([value for key,value in cave.items() if key.y == 10].count(CLEAR))
  #print([value for key,value in cave.items() if key.y == 2000000].count(CLEAR))
  xmin,xmax,_,_ = dimensions(cave)
  maxdist = max(distance for sensor,distance in sensors)
  for y in [10,2000000]:
    safe_spots = 0
    for x in range(xmin-maxdist,xmax+maxdist+1):
      spot = P(x,y)
      if any(manhattan(sensor,spot)<=distance for sensor,distance in sensors) and cave[spot] == EMPTY:
        safe_spots += 1
      #print(x,y,cave[P(x,y)],safe_spots)
    print("row {}: {} safe spots".format(y,safe_spots))

if __name__ == "__main__":
  main()
