#!/usr/bin/python3

import fileinput
import re

TIME = 2503
#TIME = 1000
REINDEER = re.compile("(\w+) can fly (\d+) km/s for (\d+) seconds, but then must rest for (\d+) seconds.")

class Reindeer:
  def __init__(self, line):
    name, speed, duration, rest = REINDEER.match(line).groups()
    
    self.name = name
    self.speed = int(speed)
    self.duration = int(duration)
    self.rest = int(rest)
    self.points = 0

  @property
  def period(self):
    return self.duration + self.rest

  def distance(self, time):
    periods, remainder = divmod(time, self.period)
    
    return periods * self.speed * self.duration + min(remainder, self.duration) * self.speed

def get_leader(reindeer, time):
  leader = max(reindeer, key = lambda x: x.distance(time))
#  print(time, leader.name, leader.distance(time), leader.points)
  return leader

def main():
  reindeer = [ Reindeer(line) for line in fileinput.input() ]

  # part 1
  winner = get_leader(reindeer, TIME)
  
  print(winner.name)
  print(winner.distance(TIME))

  # part 2
  for time in range(TIME):
    get_leader(reindeer, time + 1).points += 1

  winner = max(reindeer, key = lambda x: x.points)

  print(winner.name)
  print(winner.points)

if __name__ == "__main__":
  main()
