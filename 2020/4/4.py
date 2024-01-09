#!/usr/bin/python3

import fileinput

KEYS = {
  "byr", "iyr", "eyr", "hgt",
  "hcl", "ecl", "pid"
}

def read_passports():

  passport = {}
  passports = []

  for line in fileinput.input():

    line = line.strip()
    
    if not line and passport:
    
      passports.append(passport)
      passport = {}

    elif line:

      for pair in line.split(" "):
        key,value = pair.split(":")
        passport[key] = value

  if passport:

    passports.append(passport)

  return passports


def check_int(teststring, length, minvalue, maxvalue):

  if len(teststring) != length or str(int(teststring)) != teststring:
    return False

  return minvalue <= int(teststring) <= maxvalue
  

def validate_passport(passport, ignore_cid = True, check_data = False):
  
  required_keys = KEYS

  if not ignore_cid:
    required_keys += "cid"

  if required_keys & set(passport.keys()) != required_keys:
    return False

  valid = True

  if check_data:

    if not check_int(passport["byr"],4,1920,2002):
      valid = False

    if not check_int(passport["iyr"],4,2010,2020):
      valid = False

    if not check_int(passport["eyr"],4,2020,2030):
      valid = False

    if passport["hgt"][-2:] == "cm":
      if not check_int(passport["hgt"][:-2],3,150,193):
        valid = False
    elif passport["hgt"][-2:] == "in":
      if not check_int(passport["hgt"][:-2],2,59,76):
        valid = False
    else:
      valid = False

    if passport["hcl"][0] != "#" or len(passport["hcl"]) != 7:
      valid = False
    for c in passport["hcl"][1:]:
      if not (c.isnumeric() or "a" <= c <= "f"):
        valid = False

    if not passport["ecl"] in [ "amb", "blu", "brn", "gry", "grn", "hzl", "oth" ]:
      valid = False

    if len(passport["pid"]) != 9:
      valid = False
    for c in passport["pid"]:
      if not c.isnumeric():
        valid = False

  return valid

  
def main():

  passports = read_passports()

  s1 = sum(map(validate_passport, passports))

  print(s1)

  s2 = sum([ validate_passport(passport, check_data = True) for passport in passports ])

  print(s2)

if __name__ == "__main__":
  main()
