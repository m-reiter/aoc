#!/usr/bin/python3

import fileinput
from collections import defaultdict

def main():
  
  all_allergens = set()
  all_ingredients = set()
  allergens_to_ingredients = {}
  ingredient_count = defaultdict(int)

  for line in fileinput.input():

    line = line.rstrip(")\n")

    ingredients, allergens = line.split(" (contains ")

    ingredients = set(ingredients.split())
    allergens = set(allergens.split(", "))

    all_allergens |= allergens
    all_ingredients |= ingredients

    for allergen in allergens:
      if allergen not in allergens_to_ingredients.keys():
        allergens_to_ingredients[allergen] = set(ingredients)
      else:
        allergens_to_ingredients[allergen] &= ingredients

    for ingredient in ingredients:
      ingredient_count[ingredient] += 1

  clean = False
    
  while not clean:
    
    univocal = [x for x in allergens_to_ingredients.items() if len(x[1]) == 1]

    for allergen, ingredient in univocal:

      ingredient = ingredient.pop()

      for ingredients in allergens_to_ingredients.values():
        if type(ingredients) == set:
          ingredients.discard(ingredient)

      allergens_to_ingredients[allergen] = ingredient
      
    clean = len(univocal) == 0

  safe_ingredients = all_ingredients - set(allergens_to_ingredients.values())

  print(sum(ingredient_count[x] for x in safe_ingredients))

  canonical_list = ",".join(x[1] for x in sorted(allergens_to_ingredients.items()))

  print(canonical_list)

if __name__ == "__main__":
  main()
