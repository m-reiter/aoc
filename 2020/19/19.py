#!/usr/bin/python3

import fileinput
from itertools import product
from more_itertools import split_at

class Rules:

  def __init__(self, input_):

    self.rules = {}
    self.loops = set()

    for line in input_:
      self.parse_rule(line.strip())

  def parse_rule(self, line):

    self.valid_messages = {}

    num, rule = line.split(": ")

    self.rules.pop(num, None)
    self.rules.pop(num+"l", None)
    self.rules.pop(num+"r", None)
    self.loops.discard(num)
    
    if rule.startswith('"'):

      self.rules[num] = eval(rule)

    else:

      rules = []
      
      for subrule in rule.split(" | "):
      
        parts = subrule.split()
        
        if num not in parts:
        
          rules.append(parts)
          
        else:
          
          i = parts.index(num)
          
          self.loops.add(num)

          self.parse_rule(num+"l: "+(" ".join(parts[:i]) if i > 0 else '""'))
          self.parse_rule(num+"r: "+(" ".join(parts[i+1:]) if i < len(parts)-1 else '""'))
          
        self.rules[num] = rules

  def get_valid_messages(self, num):

    if not num in self.valid_messages.keys():
    
      rule = self.rules[num]
        
      if type(rule) == str:

        valid_messages = [rule]

      else:

        valid_messages = []

        for subrule in rule:

          valid_messages += ["".join(x) for x in product(*[self.get_valid_messages(n) for n in subrule])]

      self.valid_messages[num] = valid_messages

    return self.valid_messages[num]

  def check_rule(self, message, num):

    if message in self.get_valid_messages(num):

      return True

    if num in self.loops:

      return any(message.startswith(left)
             and message.endswith(right)
             and self.check_rule(message[len(left):len(message)-len(right)], num)
             for left, right in product(self.get_valid_messages(num+"l"), self.get_valid_messages(num+"r")))

    rules = self.rules[num]

    if len(rules) != 1 or len(rules[0]) != 2 or not any([x in self.loops for rule in self.rules[num] for x in rule]):

      return False

    parts = rules[0]

    return any(self.check_rule(message[:i], parts[0]) and self.check_rule(message[i:], parts[1]) for i in range(len(message)))
      

def main():
  
  rules, messages = split_at(fileinput.input(), lambda x: x.strip() == "")

  rules = Rules(rules)

  print(sum(rules.check_rule(message.strip(), "0") for message in messages))
  
  rules.parse_rule("8: 42 | 42 8")
  rules.parse_rule("11: 42 31 | 42 11 31")

  print(sum(rules.check_rule(message.strip(), "0") for message in messages))

if __name__ == "__main__":
  main()
