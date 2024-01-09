#!/usr/bin/python3

import fileinput
import re

DIGIT = re.compile("[1-9]")

WORDS_TO_DIGITS = {
  'one':    '1ne',
  'two':    '2wo',
  'three':  '3hree',
  'four':   '4our',
  'five':   '5ive',
  'six':    '6ix',
  'seven':  '7even',
  'eight':  '8ight',
  'nine':   '9ine'
}

DWORDS = re.compile("|".join(WORDS_TO_DIGITS))

def main():
  calibrations = [ line.strip() for line in fileinput.input() ]

  print(sum(int("".join(DIGIT.findall(calibration)[i] for i in (0,-1))) for calibration in calibrations))

  # part 2
  corrected = []
  for calibration in calibrations:
    while True:
      calibration,count = DWORDS.subn(lambda x: WORDS_TO_DIGITS[x.group(0)], calibration)
      if count == 0:
        break
    corrected.append(calibration)

  print(sum(int("".join(DIGIT.findall(calibration)[i] for i in (0,-1))) for calibration in corrected))

if __name__ == "__main__":
  main()
