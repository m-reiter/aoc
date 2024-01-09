#!/usr/bin/python3

import fileinput
import re

from itertools import product
from functools import reduce
from operator import mul

INGREDIENT = re.compile("(\w+): capacity (-?\d+), durability (-?\d+), flavor (-?\d+), texture (-?\d+), calories (\d+)")

def read_ingredients():
  ingredients = []

  for line in fileinput.input():
    name, *properties = INGREDIENT.match(line).groups()
    properties = map(int, properties)
    ingredients.append((name, *properties))

  return ingredients

def score(recipe, ingredients, calory_constraint = None):
  properties = [ 0 ] * 5

  for amount, ingredient in zip(recipe, ingredients):
    for i, modifier in enumerate(ingredient[1:]):
      properties[i] += amount * modifier

  if calory_constraint and properties[-1] != calory_constraint:
    return 0

  properties = [ max(p, 0) for p in properties ]

  return reduce(mul, properties[:4])

def main():
  ingredients = read_ingredients()
  print(ingredients)

  #recipes = [ p for p in product(*[range(101) for _ in range(len(ingredients))]) if sum(p) == 100 ]
  recipes = [ p for p in product(range(101), repeat = len(ingredients)) if sum(p) == 100 ]
  print(len(recipes))
  print(recipes[:10])

  # part 1
  winner = max(recipes, key = lambda x: score(x, ingredients))
  print(winner)
  print(score(winner, ingredients))

  # part 2
  winner = max(recipes, key = lambda x: score(x, ingredients,500))
  print(winner)
  print(score(winner, ingredients))

if __name__ == "__main__":
  main()
