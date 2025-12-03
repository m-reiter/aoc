#!/usr/bin/python3

import fileinput
import itertools

WEAPONS = """
Weapons:    Cost  Damage  Armor
Dagger        8     4       0
Shortsword   10     5       0
Warhammer    25     6       0
Longsword    40     7       0
Greataxe     74     8       0
"""

ARMORS = """
Armor:      Cost  Damage  Armor
Leather      13     0       1
Chainmail    31     0       2
Splintmail   53     0       3
Bandedmail   75     0       4
Platemail   102     0       5
"""

RINGS = """
Rings:      Cost  Damage  Armor
Damage +1    25     1       0
Damage +2    50     2       0
Damage +3   100     3       0
Defense +1   20     0       1
Defense +2   40     0       2
Defense +3   80     0       3
"""

class EquipmentItem:
  def __init__(self, description):
    columns = description.split()
    self.name = " ".join(columns[:-3])
    self.cost = int(columns[-3])
    self.damage = int(columns[-2])
    self.armor = int(columns[-1])

  def __repr__(self):
    return f'{self.__class__.__name__}("{self.name:11}  {self.cost:3}  {self.damage:3}  {self.armor:3}")'

class Player:
  def __init__(self, weapon, armor, rings):
    self.equipment = [ weapon ]
    if armor:
      self.equipment.append(armor)
    if rings:
      self.equipment += rings

    self.hitpoints = 100

    self.cost = sum(item.cost for item in self.equipment)
    self.damage = sum(item.damage for item in self.equipment)
    self.armor = sum(item.armor for item in self.equipment)

  def __str__(self):
    return f"Player (damage: {self.damage:2}, armor: {self.armor:2}, cost: {self.cost:3}) with {", ".join(item.name for item in self.equipment)}"

class Boss:
  def __init__(self, hitpoints, damage, armor):
    self.hitpoints = hitpoints
    self.damage = damage
    self.armor = armor

  def __repr__(self):
    return f"Boss(hitpoints = {self.hitpoints}, damage = {self.damage}, armor = {self.armor})"

def battle(player, boss):
  """Returns True if player wins, False if boss wins"""
  player_damage = max(player.damage - boss.armor, 1) # damage player deals to boss per round
  boss_damage = max(boss.damage - player.armor, 1)

  player_rounds, player_remainder = divmod(player.hitpoints, boss_damage)
  if player_remainder:
    player_rounds += 1
  boss_rounds, boss_remainder = divmod(boss.hitpoints, player_damage)
  if boss_remainder:
    boss_rounds += 1

  return player_rounds >= boss_rounds

def main():
  weapons = [ EquipmentItem(line) for line in WEAPONS.split("\n")[2:-1] ]
  armors = [ EquipmentItem(line) for line in ARMORS.split("\n")[2:-1] ]
  rings = [ EquipmentItem(line) for line in RINGS.split("\n")[2:-1] ]

  hitpoints, damage, armor = map(lambda x: int(x.split(":")[1]), fileinput.input())
  boss = Boss(hitpoints, damage, armor)

  winning_costs = set()
  losing_costs = set()
  for weapon in weapons:
    for armor in armors + [ None ]:
      for number_of_rings in (0,1,2):
        for player_rings in itertools.combinations(rings,number_of_rings):
          player = Player(weapon, armor, player_rings)
          if battle(player, boss):
            winning_costs.add(player.cost)
          else:
            losing_costs.add(player.cost)

  # part 1
  print(min(winning_costs))

  # part 2
  print(max(losing_costs))

if __name__ == "__main__":
  main()
