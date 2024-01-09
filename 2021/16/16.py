#!/usr/bin/python3

import fileinput

from attr import attrs, attrib
from functools import reduce

from operator import mul

LITERAL = 4
STOP = 0
TOTAL_BITS = 0

SUM = 0
PRODUCT = 1
MINIMUM = 2
MAXIMUM = 3
GREATER_THAN = 5
LESS_THAN = 6
EQUAL = 7

FUNCTIONS = {
  SUM: sum,
  PRODUCT: lambda values: reduce(mul, values),
  MINIMUM: min,
  MAXIMUM: max,
  GREATER_THAN: lambda values: int(values[0] > values[1]),
  LESS_THAN: lambda values: int(values[0] < values[1]),
  EQUAL: lambda values: int(values[0] == values[1])
}

def get_bits(string, *lengths):
  parts = []
  position = 0

  for length in lengths:
    parts.append(int(string[position:position + length], 2))
    position += length

  parts.append(string[position:])

  return parts

@attrs
class Packet:
  version = attrib()
  typeID = attrib()
  value = attrib(default = None)
  subpackets = attrib(factory = list)

  @classmethod
  def from_binary(cls, string):
    version, typeID, string = get_bits(string, 3, 3)

    if typeID == LITERAL:
      valuestring = ""

      while True:
        flag, fragment, string = get_bits(string, 1, 4)
        valuestring += "{:04b}".format(fragment)
        if flag == STOP:
          break

      return cls(version, typeID, int(valuestring, 2)), string

    else: # operator packet
      length_type, string = get_bits(string, 1)

      subpackets = []

      if length_type == TOTAL_BITS:
        length, string = get_bits(string, 15)

        old_length = len(string)

        while old_length - len(string) < length:
          subpacket, string = Packet.from_binary(string)
          subpackets.append(subpacket)

      else: # length is given in number of subpackets
        length, string = get_bits(string, 11)

        for _ in range(length):
          subpacket, string = Packet.from_binary(string)
          subpackets.append(subpacket)

      return cls(version, typeID, subpackets = subpackets), string

  @classmethod
  def from_hex(cls, string):
    return cls.from_binary("".join("{:04b}".format(int(char, 16)) for char in string))

  @property
  def version_sum(self):
    return self.version + sum(packet.version_sum for packet in self.subpackets)

  def get_value(self):
    if self.typeID == LITERAL:
      return self.value
    else:
      return FUNCTIONS[self.typeID](list(map(Packet.get_value, self.subpackets)))

def main():
  for line in fileinput.input():
    packet, remainder = Packet.from_hex(line.strip())

    assert set(remainder) <= { "0" }

    # part 1
    print(packet.version_sum)

    # part 2
    print(packet.get_value())

if __name__ == "__main__":
  main()
