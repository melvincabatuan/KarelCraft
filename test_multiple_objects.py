from karelcraft.karelcraft import *
import random

def get_color():
  '''
  Returns a random color
  '''
  colors = ["red","black","cyan","white", \
    "smoke", "green", "light_gray", "magenta", \
    "orange", "pink",  "blue","yellow", "lime", \
    "turquoise", "azure", "violet", "brown", \
    "olive", "peach", "gold", "salmon"
    ]
  return random.choice(colors)

def turn_around():
    turn_left()
    turn_left()

def turn_right():
    turn_left()
    turn_left()
    turn_left()

def main():
  move()
  for _ in range(10):
    put_beeper()

  for _ in range(10):
    pick_beeper()

  pick_beeper()



if __name__ == "__main__":
  run_karel_program()
