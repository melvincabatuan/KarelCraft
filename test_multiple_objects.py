from karelcraft.karelcraft import *
import random

MODE = 'beeper'
# MODE = 'block'

def turn_around():
    turn_left()
    turn_left()

def turn_right():
    turn_left()
    turn_left()
    turn_left()

def main():
  num_items = 5
  while front_is_clear():
    for _ in range(num_items):
      if MODE == 'block':
        put_block()
      else:
        put_beeper()
    move()

  # fencepost
  for _ in range(num_items):
    if MODE == 'block':
      put_block()
    else:
      put_beeper()

  turn_around()

  while front_is_clear():
    for _ in range(num_items):
      if MODE == 'block':
        destroy_block()
      else:
        pick_beeper()
    move()

  for _ in range(num_items):
    if MODE == 'block':
      destroy_block()
    else:
      pick_beeper()

  # Should give an exception
  if MODE == 'block':
    destroy_block()
  else:
    pick_beeper()




if __name__ == "__main__":
  run_karel_program()
