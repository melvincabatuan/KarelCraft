from karelcraft.karelcraft import *

def turn_right():
  turn_left()
  turn_left()
  turn_left()

def turn_around():
  turn_left()
  turn_left()

def go_back():
  turn_around()
  while front_is_clear():
    move()
  turn_right()

def install_beepers():
  put_beeper()
  while front_is_clear():
    move()
    if front_is_clear():
      move()
      put_beeper()

def main():
  # Special case for 1 column:
  if front_is_blocked():
    turn_left()
    install_beepers()
  # Two or more columns
  else:
    # Base-case
    install_beepers()
    go_back()
    # Inductive
    while front_is_clear():
      if beeper_present() and front_is_clear():
        move()
        turn_right()
        move()
        install_beepers()
        go_back()
      if no_beeper_present() and front_is_clear():
        move()
        turn_right()
        install_beepers()
        go_back()


if __name__ == "__main__":
  run_karel_program('7x7')
