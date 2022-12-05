#!/usr/bin/python3

import fileinput

def read_data():
  with fileinput.input() as f:
    first = f.readline()
    number_of_bits = len(first.strip())
    data = [ int(first,2) ]
    data.extend([int(line,2) for line in f])
  return number_of_bits,data

def get_most_common(number_of_bits,report):
  n_readings = len(report)
  counts = []
  for exponent in range(number_of_bits):
    counts.append(sum(line & 2**exponent for line in report)/2**exponent)
  return [ 1 if count >= n_readings / 2 else 0 for count in counts]

def filter(number_of_bits,report,bit_criterium):
  exponent = number_of_bits - 1
  while len(report) > 1:
    most_common = get_most_common(number_of_bits,report)
    report = [ record for record in report if bit_criterium(record & 2**exponent, most_common[exponent] * 2**exponent) ]
    exponent -= 1
  return(report)

def part1(number_of_bits,report):
  most_common = get_most_common(number_of_bits,report)
  gamma = sum(digit * 2**exponent for exponent,digit in enumerate(most_common))
  epsilon = sum((1-digit) * 2**exponent for exponent,digit in enumerate(most_common))
  return gamma*epsilon

def part2(number_of_bits,report):
  oxygen = filter(number_of_bits,report,lambda x,y: x == y)[-1]
  co2 = filter(number_of_bits,report,lambda x,y: x != y)[-1]
  return(oxygen*co2)

def main():
  number_of_bits,report = read_data()
  print(part1(number_of_bits,report))
  print(part2(number_of_bits,report))

if __name__ == "__main__":
  main()
