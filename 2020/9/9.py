#!/usr/bin/python3

import fileinput

class Xmas():

  def __init__(self,code):

    self.sums = []
    
    for i in range(24):
      self.sums.append([code[i]+code[j] for j in range(i+1,25)])
       
    self.code = code
    self.position = 25

  def parse_next(self):
    
    num = self.code[self.position]

    if not any([num in x for x in self.sums]):
      return num

    self.sums.pop(0)
    self.sums.append([])

    for i in range(24):
      self.sums[i].append(self.code[self.position-24+i]+num)

    self.position +=1

    return True

  def find_sum(self,num):

    for i in range(len(self.code)):
      
      excerpt = []
      j = 0
      
      while sum(excerpt) < num:
        excerpt.append(self.code[i+j])
        j += 1
      
      if sum(excerpt) == num:
        return excerpt
    
def main():
  
  code = [int(line) for line in fileinput.input()]
  
  xmas = Xmas(code)

  ans = xmas.parse_next()
  while ans == True:
    ans = xmas.parse_next()

  print(ans)

  excerpt = xmas.find_sum(ans)

  print(excerpt)
  print(min(excerpt))
  print(max(excerpt))
  print(min(excerpt)+max(excerpt))

if __name__ == "__main__":
  main()
