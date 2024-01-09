#!/usr/bin/python3

import fileinput

INPUT = 846601
TEST_CASES = [
  (9,"5158916779"),
  (5,"0124515891"),
  (18,"9251071085"),
  (2018,"5941429882")
]

def play(number,search_string=None):
  scores = [3, 7]
  current = [0, 1]

  while True:
    for char in str(sum(scores[i] for i in current)):
      scores.append(int(char))
    current = [ (position + 1 + scores[position]) % len(scores) for position in current ]
    if search_string is None:
      if len(scores) >= number + 10:
        return "".join(map(str,scores[number:number+10]))
    else:
      if search_string in "".join(map(str,scores[-len(search_string)-1:])):
        compound = "".join(map(str,scores))
        return compound.index(search_string)
  
def main():
  for number,result in TEST_CASES:
    assert(play(number) == result)
  print(play(INPUT))

  for result,search_string in TEST_CASES:
    assert(result == play(0,search_string))
  print(play(0,str(INPUT)))

if __name__ == "__main__":
  main()
