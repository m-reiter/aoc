#!/usr/bin/python3

import fileinput

HEADINGS = [ "e", "s", "w", "n" ]

class Ship():

  def __init__(self):

    self.northsouth = 0
    self.eastwest = 0

    self.heading = "e"

  def n(self, value):

    self.northsouth += value

  def s(self, value):

    self.northsouth -= value

  def e(self, value):

    self.eastwest += value

  def w(self, value):

    self.eastwest -= value

  def f(self, value):

    self.__getattribute__(self.heading)(value)

  def l(self, value):

    currentindex = HEADINGS.index(self.heading)

    newindex = (currentindex - value//90) % len(HEADINGS)

    self.heading = HEADINGS[newindex]

  def r(self, value):

    currentindex = HEADINGS.index(self.heading)

    newindex = (currentindex + value//90) % len(HEADINGS)

    self.heading = HEADINGS[newindex]

  def manhattan(self):

    return abs(self.northsouth)+abs(self.eastwest)

  def follow(self, instruction):

    action = instruction[0].lower()
    value = int(instruction[1:])

    self.__getattribute__(action)(value)


class WaypointShip(Ship):

  def __init__(self):

    super().__init__()

    self.waypoint = [10,1]

  def n(self, value):

    self.waypoint[1] += value

  def s(self, value):

    self.waypoint[1] -= value

  def e(self, value):

    self.waypoint[0] += value

  def w(self, value):

    self.waypoint[0] -= value

  def f(self, value):

    self.northsouth += value*self.waypoint[1]
    self.eastwest += value*self.waypoint[0]

  def left90(self):

    x,y = self.waypoint

    self.waypoint[0] = -y
    self.waypoint[1] = x

  def l(self, value):

    for i in range(value//90):
      self.left90()

  def r(self, value):

    for i in range(4 - value//90):
      self.left90()


def main():
  
  instructions = list(fileinput.input())

  ship = Ship()

  for line in instructions:

    ship.follow(line)

  print(ship.manhattan())

  ship = WaypointShip()

  for line in instructions:

    ship.follow(line)

  print(ship.manhattan())


if __name__ == "__main__":
  main()
