#!/usr/bin/python3

import fileinput

BRACKETS = {
  ")": ("(",3),
  "]": ("[",57),
  "}": ("{",1197),
  ">": ("<",25137)
}
CLOSING_SCORES = {"(": 1, "[": 2, "{": 3, "<": 4}

def check_line(line):
  open_brackets = []
  for character in line.strip():
    if character in BRACKETS.keys():
      if open_brackets[-1] == BRACKETS[character][0]:
        open_brackets.pop()
      else:
        # line is corrupt, return positive score
        return BRACKETS[character][1],None
    else:
      open_brackets.append(character)
  # return 0 if line is correct, negative value if incomplete
  return -len(open_brackets),open_brackets

def parts(subsystem):
  total = 0
  line_scores = []
  for line in subsystem:
    checksum,open_brackets = check_line(line)
    if checksum > 0:
      total += checksum
    elif checksum < 0:
      line_score = 0
      for bracket in reversed(open_brackets):
        line_score *= 5
        line_score += CLOSING_SCORES[bracket]
      line_scores.append(line_score)
  line_scores.sort()
  return total,line_scores[len(line_scores) // 2]

def main():
  subsystem = list(fileinput.input())
  part1,part2 = parts(subsystem)
  print(part1)
  print(part2)

if __name__ == "__main__":
  main()
