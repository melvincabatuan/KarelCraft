'''
This tests the stacking logic for mixed objects - blocks, paints, beepers
@author: MKC
'''

from karelcraft.karelcraft import *
import random

OPTIONS = ('block', 'beeper', 'paint')

def turn_around():
    turn_left()
    turn_left()

def turn_right():
    turn_left()
    turn_left()
    turn_left()

def main():
  while front_is_clear():
    for _ in range(6):
      mode = random.choice(OPTIONS)
      if mode == 'block':
        put_block()
      elif mode == 'beeper':
        put_beeper()
      else:
        paint_corner('red')
    move()
    if front_is_blocked():
      turn_left()
    if beeper_present() or color_present() or block_present():
      break

if __name__ == "__main__":
  run_karel_program('8x8')
