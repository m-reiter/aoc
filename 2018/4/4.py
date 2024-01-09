#!/usr/bin/python3

import fileinput
import re
from datetime import datetime
from collections import defaultdict

GUARD = re.compile("Guard #(\d+) begins shift")

def main():
  observations = sorted(list(fileinput.input()))

  total_minutes = defaultdict(int)
  guard_minutes = defaultdict(lambda: defaultdict(int))
  guard = "nobody"
  last_minute = 59
  awake = True

  for line in observations:
    time,observation = line.strip().split("] ")
    is_guard = GUARD.match(observation)
    if is_guard:
      if not awake:
        total_minutes[guard] += 59-last_minute
        for minute in range(last_minute,60):
          guard_minutes[guard][minute] += 1
      guard = is_guard.group(1)
      awake = True
      last_minute = 0
    else:
      now_minute = datetime.strptime(time,"[%Y-%m-%d %H:%M").minute
      awake = not awake
      if awake:
        total_minutes[guard] += now_minute-last_minute
        for minute in range(last_minute,now_minute):
          guard_minutes[guard][minute] += 1
      last_minute = now_minute

  sleeper = max(total_minutes.keys(), key = lambda x: total_minutes[x])
  sweetspot = max(guard_minutes[sleeper].keys(), key = lambda x: guard_minutes[sleeper][x])

  print(int(sleeper)*sweetspot)

  sleeper2 = max(guard_minutes.keys(), key = lambda x: max(guard_minutes[x].values()))
  sweetspot2 = max(guard_minutes[sleeper2].keys(), key = lambda x: guard_minutes[sleeper2][x])

  print(int(sleeper2)*sweetspot2)

if __name__ == "__main__":
  main()
