'''
Classic stonemason problem
@MKC
'''

from karelcraft.karelcraft import *

def turn_right():
  turn_left()
  turn_left()
  turn_left()

def turn_around():
  turn_left()
  turn_left()

def install_beepers():
  turn_left()
  while front_is_clear():
    if no_beeper_present():
      put_beeper()
    move()
  if no_beeper_present():
    put_beeper()
  turn_around()

def go_back_to_ground():
  while front_is_clear():
    move()
  turn_left()

def go_to_next_column():
  '''
  Potential issue here when front is not clear
  However, this problem is written under the ff. assumptions:
  - final column will always have a wall immediately after it
  - columns are always exactly four avenues apart
  '''
  move()
  move()
  move()
  move()

def main():
  while front_is_clear():
    install_beepers()
    go_back_to_ground()
    go_to_next_column()

  # Fencepost
  install_beepers()


if __name__ == "__main__":
  run_karel_program('stone_mason_karel')
