#!/usr/bin/python3

import fileinput

def spin(sequence, number):
  return sequence[-number:]+sequence[:len(sequence)-number]

def swap(sequence, positions):
  a,b = sorted(positions)

  sequence[a:b+1:b-a] = reversed(sequence[a:b+1:b-a])
  return sequence

def dance(instructions, programs):
  if programs is None:
    programs = [chr(ord("a")+i) for i in range(length)]
  
  for step in instructions:
    if step.startswith("s"):
      programs = spin(programs, int(step[1:]))
    else:
      if step.startswith("x"):
        positions = map(int,step[1:].split("/"))
      elif step.startswith("p"):
        positions = (programs.index(x) for x in step[1:].split("/"))
      programs = swap(programs, positions)

  return programs

def main():
  instructions = fileinput.input().readline().strip().split(",")

  # part 1
  programs = [chr(ord("a")+i) for i in range(16 if len(instructions) > 10 else 5)]
  programs = dance(instructions, programs)
  print("".join(programs))

  # part 2
  programs = [chr(ord("a")+i) for i in range(16 if len(instructions) > 10 else 5)]
  programs = dance([i for i in instructions if i.startswith("p")], programs)
  p_permutations = {
    chr(ord("a")+i): programs[i] for i in range(len(programs))
  }

  programs = list(range(len(programs)))
  programs = dance([i for i in instructions if not i.startswith("p")], programs)
  other_permutations = {
    i: programs[i] for i in range(len(programs))
  }

  for _i in range(9):
    programs = [chr(ord("a")+i) for i in range(16 if len(instructions) > 10 else 5)]
    for _j in range(10):
      programs = [ p_permutations[char] for char in programs ]
    p_permutations = {
      chr(ord("a")+i): programs[i] for i in range(len(programs))
    }
    programs = list(range(len(programs)))
    for _j in range(10):
      programs = [ programs[other_permutations[i]] for i in range(len(programs)) ]
    other_permutations = {
      i: programs[i] for i in range(len(programs))
    }
      
  programs = [chr(ord("a")+i) for i in range(16 if len(instructions) > 10 else 5)]
  programs = [ p_permutations[char] for char in programs ]
  programs = [ programs[other_permutations[i]] for i in range(len(programs)) ]
  print("".join(programs))

if __name__ == "__main__":
  main()
