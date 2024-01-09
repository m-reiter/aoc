#!/usr/bin/python3

import fileinput

TEST_INPUT = [
"L.LL.LL.LL",
"LLLLLLL.LL",
"L.L.L..L..",
"LLLL.LL.LL",
"L.LL.LL.LL",
"L.LLLLL.LL",
"..L.L.....",
"LLLLLLLLLL",
"L.LLLLLL.L",
"L.LLLLL.LL"
]

DIRECTIONS = [(i,j) for i in range(-1,2) for j in range(-1,2) if i or j]

class Seats():

  def __init__(self, lines, to_next_seen = False, occupied_to_leave = 4):

    self.read_seats(lines)

    self.to_next_seen = to_next_seen
    self.occupied_to_leave = occupied_to_leave

  def read_seats(self, lines):

    self.seats = [line.strip()+"X" for line in lines]

    self.seats.append("X"*(self.dimx+1))

  def __str__(self):

    return "\n".join([line[:-1] for line in self.seats[:-1]])

  @property
  def dimx(self):
    return len(self.seats[0])-1
  
  @property
  def dimy(self):
    return len(self.seats)-1

  def get(self, x, y):
  
    return self.seats[y][x]
  
  def is_seat(self, x, y):
  
    return self.get(x, y) in "#L"
  
  def is_occupied(self, x, y):
  
    return self.get(x,y) == "#"

  def is_empty(self, x, y):
  
    return self.get(x,y) == "L"

  def is_margin(self, x, y):

    return self.get(x,y) == "X"
  
  def get_neighbors(self,x,y):
    
    neighbors = []

    for xoffset,yoffset in DIRECTIONS:
      i = 1
      while not self.is_margin(x+i*xoffset, y+i*yoffset):
        if self.is_seat(x+i*xoffset, y+i*yoffset):
          neighbors.append((x+i*xoffset, y+i*yoffset))
          break
        elif self.to_next_seen:
          i += 1
        else:
          break

    return neighbors
  
  def count_occupied_neighbors(self,x,y):

    count = 0

    for x1,y1 in self.get_neighbors(x,y):
    
      if self.is_occupied(x1,y1):
        count += 1

    return count
      
  def iterate(self):

    changed = False
    newseats = []

    for y in range(self.dimy):

      row = ""

      for x in range(self.dimx):

        occupied_neighbors = self.count_occupied_neighbors(x,y)

        if self.is_empty(x,y) and occupied_neighbors == 0:
          row += "#"
        elif self.is_occupied(x,y) and occupied_neighbors >= self.occupied_to_leave:
          row += "L"
        else:
          row += self.get(x,y)
      
      if row != self.seats[y][:-1]:
        changed = True

      newseats.append(row)

    if changed:
      self.read_seats(newseats)
    
    return changed

  def run_until_stable(self):

    changed = True

    while changed:
      changed = self.iterate()

  def count_occupied_seats(self):

    return sum([line.count("#") for line in self.seats])

def main():
  
  layout = list(fileinput.input())

  seats = Seats(layout)

  seats.run_until_stable()

  print(seats.count_occupied_seats())

  seats = Seats(layout, to_next_seen = True, occupied_to_leave = 5)
#  seats = Seats(TEST_INPUT, to_next_seen = True, occupied_to_leave = 5)

  seats.run_until_stable()

  print(seats.count_occupied_seats())

if __name__ == "__main__":
  main()
