#!/usr/bin/python3

from hashlib import md5

INPUT = "yzbqklnj"

TEST_CASES = {
  "abcdef": 609043,
  "pqrstuv": 1048970
}

def get_lowest_number(key,zeroes=5):
  lowest = 1
  while True:
    if md5("{}{}".format(key,lowest).encode()).hexdigest().startswith("0"*zeroes):
      return lowest
    lowest += 1

def main():
  for key,result in TEST_CASES.items():
    assert get_lowest_number(key) == result

  print(get_lowest_number(INPUT))
  print(get_lowest_number(INPUT,6))

if __name__ == "__main__":
  main()
