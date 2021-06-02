from karelcraft.karelcraft import *
import random

TEXTURES = ('grass','stone','brick','dirt','lava', 'rose', \
          'dlsu', 'diamond', 'emerald', 'gold', 'obsidian', \
          'leaves', 'sand', 'wood', 'stonebrick', 'sponge', 'snow')

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

def go_to_wall():
  '''
  pre: Karel is anywhere inside the world
  post:Karel will be located at the front of the wall its facing
  '''
  while front_is_clear():
    move()

def put_color_line(n):
  '''
  Put colors to a n squares in a row
  '''
  for _ in range(n):
    texture = random.choice(TEXTURES)
    put_block(texture)
    # paint_corner(get_color())
    # put_beeper()
    move()

def go_to_next_step(step):
  '''
  pre: Karel is facing the wall to West
  post: Karel is in the next step facing East
  '''
  turn_right()
  move()
  turn_right()
  for i in range(step):
    if front_is_clear():
      move()

def pyramid():
  '''
  Pre: Initial Karel world
  Post: Pyramid of colors (built from bottom to top)
  '''
  # Install base layer and measure the width base
  width = 1
  while front_is_clear():
    # paint_corner(get_color())
    texture = random.choice(TEXTURES)
    put_block(texture)
    # put_beeper()
    move()
    width += 1

  # paint_corner(get_color())
  texture = random.choice(TEXTURES)
  put_block(texture)
  # put_beeper()
  turn_around()
  go_to_wall()

  # Installation of the rest of tbase.graphicsEngine.removeAllWindows()he levels: 2 - onward
  step = 1
  while right_is_clear() and width > 0:
    go_to_next_step(step)

    width -= 2
    put_color_line(width)
    turn_around()
    go_to_wall()
    step += 1


def main():
  pyramid()


if __name__ == "__main__":
  run_karel_program()
