from karelcraft.karelcraft import *

def turn_right():
  turn_left()
  turn_left()
  turn_left()

def turn_around():
  turn_left()
  turn_left()

def go_to_beeper():
  move()
  move()
  turn_right()
  move()
  turn_left()
  move()

def go_back_to_house():
  turn_around()
  move()
  move()
  move()
  turn_right()
  move()
  turn_right()

def main():
  go_to_beeper()
  pick_beeper()
  go_back_to_house()

if __name__ == "__main__":
  run_karel_program('collect_newspaper_karel')
