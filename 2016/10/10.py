#!/usr/bin/python3

import fileinput
import re
from collections import defaultdict

GIVE=re.compile("bot (\d+) gives low to (bot|output) (\d+) and high to (bot|output) (\d+)")
ASSIGN=re.compile("value (\d+) goes to bot (\d+)")

def step(bots,instructions):
  givers = [ bot for bot in instructions if len(bots[bot]) == 2 ]
  if not givers:
    return False
  bot = givers[0]
  bots[instructions[bot][0]].append(min(bots[bot]))
  bots[instructions[bot][1]].append(max(bots[bot]))
  bots[bot] = list()
  return True

def run_parts(bots,instructions,target={2,5}):
  while True:
    for bot,items in bots.items():
      if set(items) == target:
        comparer = bot
    if not step(bots,instructions):
      break
  return comparer,bots[1000][0]*bots[1001][0]*bots[1002][0]

def parse_input(input):
  bots = defaultdict(list)
  instructions = {}
  max_bot = 0
  for line in input:
    match = GIVE.match(line)
    if match:
      giver,bot_or_output1,recipient1,bot_or_output2,recipient2 = match.groups()
      giver = int(giver)
      max_bot = max(max_bot,giver)
      recipient1 = int(recipient1)
      recipient2 = int(recipient2)
      if bot_or_output1 == "output":
        recipient1 += 1000
      else:
        max_bot = max(max_bot,recipient1)
      if bot_or_output2 == "output":
        recipient2 += 1000
      else:
        max_bot = max(max_bot,recipient2)
      instructions[giver] = (recipient1,recipient2)
    else:
      match = ASSIGN.match(line)
      if match:
        value,bot = map(int,match.groups())
        max_bot=max(max_bot,bot)
        bots[bot].append(value)
      else:
        raise ValueError
  return bots,instructions

def main():
  input = [ line.strip() for line in fileinput.input() ]
  bots,instructions = parse_input(input)
  part1,part2 = run_parts(bots,instructions,target={17,61})
  print(part1)
  print(part2)

if __name__ == "__main__":
  main()
