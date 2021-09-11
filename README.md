# KarelCraft

Karel + 'MineCraft' - like environment enabled by Ursina Engine (Panda3D) 

![](https://github.com/melvincabatuan/KarelCraft/blob/master/screenshots/KarelCraft13.PNG)

"Karel the Robot", an educational programming language for beginners (Pattis, 1970),
remain useful for learners in programming and computational thinking. In it's most 
recent form, you can use it to learn the multi-purpose language Python that is popular 
in data science and machine learning community. On the other hand, Minecraft (by Mojang Studios) 
and other similar sandbox construction video games (e.g. Minetest) are popular to gamers 
and have built a considerable following in the community.

KarelCraft is an attempt to mix the ideas together and come up with an environment that
beginner programmers can learn fundamental programming skills, while working with an agent,
i.e. Karel, doing actions and performing decisions in a small sandbox construction setting.  

### Install

```sh
pip install git+https://github.com/melvincabatuan/KarelCraft.git
```

### Uninstall

```sh
pip uninstall karelcraft
```

Sample screenshots:

### Karel Building Blocks around the Perimeter of the world

![](https://github.com/melvincabatuan/KarelCraft/blob/master/screenshots/KarelCraft1.PNG)
![](https://github.com/melvincabatuan/KarelCraft/blob/master/screenshots/KarelCraft20.PNG)
![](https://github.com/melvincabatuan/KarelCraft/blob/master/screenshots/KarelCraft3.PNG)

* Source: test_karel.py
* Code:

```python
from karelcraft.karelcraft import *

def main():
    while front_is_clear():
        put_block()
        # put_beeper()
        # paint_corner('green')
        move()

        if front_is_blocked():
            turn_left()

        if block_present():
            print("Breaking...")
            break


if __name__ == "__main__":
    run_karel_program()
```

### Karel putting 'beepers' in a single line
![](https://github.com/melvincabatuan/KarelCraft/blob/master/screenshots/KarelCraft4.PNG)

```python
from karelcraft.karelcraft import *

def put_beeper_line():
  '''
  Pre: Karel at initial state (1,1) and facing East with infinite beepers
  Post: Beepers will completely fill a certain row
  '''
  while front_is_clear():
    put_beeper()
    move()
  put_beeper()

def main():
  put_beeper_line()


if __name__ == "__main__":
  run_karel_program()
```

### Karel creating a staircase pattern of beepers
![](https://github.com/melvincabatuan/KarelCraft/blob/master/screenshots/KarelCraft5.PNG)

```python
from karelcraft.karelcraft import *

def go_to_wall():
  '''
  pre: Karel is anywhere inside the world
  post:Karel will be located at the front of the wall its facing
  '''
  while front_is_clear():
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


def staircase():
  '''
  Pre: Karel at initial position, facing East (empty world)
  Post: Beepers in staircase pattern (Karel position not important)
  '''
  step = 1
  while left_is_clear() and front_is_clear():
    put_beeper_line()
    turn_around()
    go_to_wall()
    go_to_next_step(step)
    step += 1

  put_beeper_line() # handles fencepost error



def main():
  staircase()


if __name__ == "__main__":
  run_karel_program()
```

### Karel creating a staircase pattern of random colors
![](https://github.com/melvincabatuan/KarelCraft/blob/master/screenshots/KarelCraft6.PNG)

```python
import random
from karelcraft.karelcraft import *

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

def put_line():
  '''
  Put colors to a row
  '''
  while front_is_clear():
    rand_color = get_color()
    paint_corner(rand_color)
    move()

  rand_color = get_color()
  paint_corner(rand_color)

def color_staircase():
  '''
  Pre: Karel at initial position, facing East (empty world)
  Post: Beepers in staircase pattern (Karel position not important)
  '''
  step = 1
  while left_is_clear() and front_is_clear():
    put_line()
    turn_around()
    go_to_wall()
    go_to_next_step(step)
    step += 1

  put_line() # handles fencepost error


def main():
  color_staircase()


if __name__ == "__main__":
  run_karel_program()

```

### Karel creating the pyramid pattern
![](https://github.com/melvincabatuan/KarelCraft/blob/master/screenshots/KarelCraft7.PNG)

```python
from karelcraft.karelcraft import *

def put_color_line(n):
  '''
  Put colors to a n squares in a row
  '''
  for _ in range(n):
    paint_corner(get_color())
    move()

def pyramid():
  '''
  Pre: Initial Karel world
  Post: Pyramid of colors (built from bottom to top)
  '''
    # Install base layer and measure the width base
  width = 1
  while front_is_clear():
    paint_corner(get_color())
    move()
    width += 1
    print(right_is_clear())

  rand_color = get_color()
  paint_corner(rand_color)
  turn_around()
  go_to_wall()

  # Installation of the rest of the levels: 2 - onward
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

```

### Karel creating the random color pattern
![](https://github.com/melvincabatuan/KarelCraft/blob/master/screenshots/KarelCraft8.PNG)

```python
from karelcraft.karelcraft import *

def handle_column_world():
  '''
  Handles 1x1 or vertical worlds
  '''
  turn_left()
  while front_is_clear():
    paint_corner(get_color())
    move()
  paint_corner(get_color())

def handle_bigger_worlds():
  '''
  Handles world with > 2 width
  '''
  while front_is_clear():
    paint_corner(get_color())
    move()

    if front_is_blocked() and facing_east():
      paint_corner(get_color())
      turn_left()
      if front_is_clear():
        move()
        turn_left()

    if front_is_blocked() and facing_west():
      paint_corner(get_color())
      turn_right()
      if front_is_clear():
        move()
        turn_right()

def random_coloring():
  if front_is_blocked():
    handle_column_world()
  else:
    handle_bigger_worlds()


def main():
  random_coloring()


if __name__ == "__main__":
  run_karel_program()

```

### Karel creating color layering pattern
![](https://github.com/melvincabatuan/KarelCraft/blob/master/screenshots/KarelCraft9.PNG)

```python
from karelcraft.karelcraft import *

def outer_layer():
  '''
  Pre: Karel at initial position
  Post: Karel colors the perimeter
  '''
  color = get_color()
  while front_is_clear() and no_color_present():
    paint_corner(color)
    move()
    if front_is_blocked():
      turn_left()

def move_inward():
  '''
  pre: Karel at initial position (facing East) with colored perimeter
  post: Karel moves into the inner layer
  '''
  move()
  turn_left()
  move()
  turn_right()

def step_back():
  '''
  Move one step back
  '''
  turn_around()
  move()
  turn_around()

def inner_layers():
  while no_color_present():
    color = get_color()
    for _ in range(4): # Color the layer corners
      while no_color_present():
        paint_corner(color)
        move()
        if color_present():
          step_back()
          turn_left()
      if front_is_clear():
        move()

def rainbow_layers():
  outer_layer()
  move_inward()
  inner_layers()

def main():
  rainbow_layers()


if __name__ == "__main__":
  run_karel_program()

```

### Karel creating multiple blocks
![](https://github.com/melvincabatuan/KarelCraft/blob/master/screenshots/KarelCraft10.PNG)

- 4 : grass texture
- 5 : stone texture
- 6 : brick texture
- 7 : dirt texture
- 8 : lava texture

```python
from karelcraft.karelcraft import *

def handle_column_world():
  '''
  Handles 1x1 or vertical worlds
  '''
  turn_left()
  while front_is_clear():
    put_block()
    move()
  put_block()

def handle_bigger_worlds():
  '''
  Handles world with > 2 width
  '''
  while front_is_clear():
    put_block()
    move()

    if front_is_blocked() and facing_east():
      put_block()
      turn_left()
      if front_is_clear():
        move()
        turn_left()

    if front_is_blocked() and facing_west():
      put_block()
      turn_right()
      if front_is_clear():
        move()
        turn_right()

def random_coloring():
  if front_is_blocked():
    handle_column_world()
  else:
    handle_bigger_worlds()


def main():
  random_coloring()


if __name__ == "__main__":
  run_karel_program()

```

### Additional screenshots:

![](https://github.com/melvincabatuan/KarelCraft/blob/master/screenshots/KarelCraft11.PNG)

![](https://github.com/melvincabatuan/KarelCraft/blob/master/screenshots/KarelCraft12.PNG)

### Karel creating an hourglass pattern:

![](https://github.com/melvincabatuan/KarelCraft/blob/master/screenshots/KarelcraftHourglass.PNG)

```python
from karelcraft.karelcraft import *

# MODE = 'beeper'
# MODE, COLOR = 'paint', 'cyan'
MODE = 'block'

def look(direction, condition):
    while not condition():
        turn_left()

def move_forward(steps):
    for _ in range(steps):
        if front_is_clear():
            move()

def get_width():
    count = 0
    while front_is_clear():
        move()
        count += 1
    return(count)

def move_to_wall():
    while(front_is_clear()):
        move()

def install_a_beeper():
    if no_beepers_present():
        put_beeper()

def install(mode):
    if mode == 'paint':
        if no_color_present():
            paint_corner(COLOR)
    elif mode == 'block':
        if no_block_present():
            put_block()
    else:
        if no_beepers_present():
            put_beeper()

def go_to_upper_base(width):
    if width % 2 == 0:
        install(MODE)
    look("north", facing_north)
    move_forward(width//2)
    look("east", facing_east)
    move_to_wall()

# DRY Principle: Don't Repeat Yourself
def install_triangle(width, is_bottom = True):
    for i in range(width, 0, -2):
        for _ in range(i):
            look("west", facing_west)
            install(MODE)
            move()
        install(MODE)
        if is_bottom:
            look("north", facing_north)
        else:
            look("south", facing_south)
        if front_is_blocked():
            break
        move()
        look("east", facing_east)
        move_forward(i-1)


def main():
    width = get_width()
    install_triangle(width)
    go_to_upper_base(width)
    install_triangle(width, is_bottom = False)


if __name__ == "__main__":
    run_karel_program()

```


### Karel creating a 3d pyramid pattern:

![](https://github.com/melvincabatuan/KarelCraft/blob/master/screenshots/KarelCraft1.PNG)

```python
from karelcraft.karelcraft import *
import random

TEXTURES = ('grass','stone','brick','dirt','lava', 'rose', 'dlsu')

def turn_around():
    turn_left()
    turn_left()

def turn_right():
    turn_left()
    turn_left()
    turn_left()

def outer_layer():
  texture = random.choice(TEXTURES)
  while front_is_clear() and no_block_present():
    put_block(texture)
    move()
    if front_is_blocked():
      turn_left()

def move_inward():
  '''
  pre: Karel at initial position (facing East) with colored perimeter
  post: Karel moves into the inner layer
  '''
  move()
  turn_left()
  move()
  turn_right()

def step_back():
  '''
  Move one step back
  '''
  turn_around()
  move()
  turn_around()

def inner_layers():
  num = 1
  while no_block_present():
    num += 1
    texture = random.choice(TEXTURES)
    for _ in range(4):
      while no_block_present():
        for _ in range(num):
          put_block(texture)
        move()
        if block_present():
          step_back()
          turn_left()
      if front_is_clear():
        move()



def main():
  outer_layer()
  move_inward()
  inner_layers()

if __name__ == "__main__":
  run_karel_program()

```

### Karel creating a CheckerBoard pattern:

![](https://github.com/melvincabatuan/KarelCraft/blob/master/screenshots/KarelCraft20.PNG)

```python
from karelcraft.karelcraft import *
import random

# MODE = 'beeper'
# MODE, COLOR = 'paint', 'cyan'
MODE = 'block'

TEXTURES = ('grass','stone','brick','dirt','lava', 'rose', \
          'dlsu', 'diamond', 'emerald', 'gold', 'obsidian', \
          'leaves', 'sand', 'wood', 'stonebrick', 'sponge', 'snow')

def get_color():
  '''
  Returns a random color
  '''
  colors = ["red","black","cyan","white", \
    "smoke", "green", "light_gray", "gray", \
    "dark_gray", "black", "magenta", \
    "orange", "pink",  "blue","yellow", "lime", \
    "turquoise", "azure", "violet", "brown", \
    "olive", "peach", "gold", "salmon"
  ]
  return random.choice(colors)

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

def install():
  if MODE == 'block':
    texture = random.choice(TEXTURES)
    put_block(texture)
  elif MODE == 'beeper':
    put_beeper()
  elif MODE == 'paint':
    paint_corner(get_color())

  while front_is_clear():
    move()
    if front_is_clear():
      move()
      if MODE == 'block':
        texture = random.choice(TEXTURES)
        put_block(texture)
      elif MODE == 'beeper':
        put_beeper()
      elif MODE == 'paint':
        paint_corner(get_color())

def main():
  # Special case for 1 column:
  if front_is_blocked():
    turn_left()
    install()
  # Two or more columns
  else:
    # Base-case
    install()
    go_back()
    # Inductive
    while front_is_clear():
      if (beeper_present() or block_present() or color_present()) and front_is_clear():
        move()
        turn_right()
        move()
        install()
        go_back()
      if (no_beeper_present() or no_block_present() or no_color_present()) and front_is_clear():
        move()
        turn_right()
        install()
        go_back()


if __name__ == "__main__":
  run_karel_program('7x7')

```
