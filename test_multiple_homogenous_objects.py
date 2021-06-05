'''
This tests the stacking of homogenous objects - blocks, paints, beepers
@author: MKC
'''


from karelcraft.karelcraft import *
import random

MODE = 'beeper'
# MODE = 'block'
# MODE = 'paint'  # no stacking / destroy

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
      elif MODE == 'beeper':
        put_beeper()
      else:
        paint_corner('green')
    move()

  # fencepost
  for _ in range(num_items):
    if MODE == 'block':
      put_block()
    elif MODE == 'beeper':
      put_beeper()
    else:
      paint_corner('green')

  turn_around()

  while front_is_clear():
    for _ in range(num_items):
      if MODE == 'block':
        destroy_block()
      elif MODE == 'beeper':
        pick_beeper()
      else:
        remove_paint()
        break
    move()

  for _ in range(num_items):
    if MODE == 'block':
      destroy_block()
    elif MODE == 'beeper':
      pick_beeper()
    else:
      remove_paint()

  # Should give an exception (as expected)
  if MODE == 'block':
    destroy_block()
  elif MODE == 'beeper':
    pick_beeper()
  else:
    remove_paint()




if __name__ == "__main__":
  run_karel_program('8x8')
