r'''
              ___________________________________________________
            /                                                    \`
           |    _____________________________________________     |
           |   |                                             |    |
           |   |  >>> _                                      |    |
           |   |                                             |    |
           |   |             Python Refresher III            |    |
           |   |                                             |    |
           |   |                    for                      |    |
           |   |                                             |    |
           |   |                  Learners                   |    |
           |   |                                             |    |
           |   |                                             |    |
           |   |                     by                      |    |
           |   |                                             |    |
           |   |                     MKC                     |    |
           |   |_____________________________________________|    |
           |                                                      |
            \_____________________________________________________/
                   \_______________________________________/
                _______________________________________________
             _-'    .-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.  --- `-_
          _-'.-.-. .---.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.--.  .-.-.`-_
       _-'.-.-.-. .---.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-`__`. .-.-.-.`-_
    _-'.-.-.-.-. .-----.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-----. .-.-.-.-.`-_
 _-'.-.-.-.-.-. .---.-. .-----------------------------. .-.---. .---.-.-.-.`-_
:-----------------------------------------------------------------------------:
`---._.-----------------------------------------------------------------._.---'


           ___   _      _              _    _
          / _ \ | |__  (_)  ___   ___ | |_ (_)__   __ ___  ___
         | | | || '_ \ | | / _ \ / __|| __|| |\ \ / // _ \/ __|
         | |_| || |_) || ||  __/| (__ | |_ | | \ V /|  __/\__ \
          \___/ |_.__/_/ | \___| \___| \__||_|  \_/  \___||___/
                     |__/


        • To introduce Karel the Robot introductory programming
          environment to teach students the fundamental concepts
          and skills of programming.

        • To practice conditionals and iteration (while-loop) as
          applied to solving Karel the Robot problems emphasizing
          logic and structure over calculation.

        • To install a Python package with pip package manager.

        • To introduce precondition and postcondition concepts.

        • To introduce basic debugging concepts





              _      _  _                       __
   __      __| |__  (_)| |  ___  __   __ ___   / _|  ___   _ __
   \ \ /\ / /| '_ \ | || | / _ \ \ \ / // __| | |_  / _ \ | '__|
    \ V  V / | | | || || ||  __/  \ V / \__ \ |  _|| (_) || |
     \_/\_/  |_| |_||_||_| \___|   \_/  |___/ |_|   \___/ |_|







                               _
                        _ __  (_) _ __
                       | '_ \ | || '_ \
                       | |_) || || |_) |
                       | .__/ |_|| .__/
                       |_|       |_|

        a tool for installing and managing Python packages


          e.g.       pip install stanfordkarel


            Note: pip is run from the command line,
                    not the Python interpreter.
'''

# from stanfordkarel import * # Installation is successful!


r'''

                    _  __                  _
                   | |/ / __ _  _ __  ___ | |
                   | ' / / _` || '__|/ _ \| |
                   | . \| (_| || |  |  __/| |
                   |_|\_\\__,_||_|   \___||_|

          Educational programming language for beginners
                       Rich Pattis (1970)

        e.g.
                   BEGINNING-OF-PROGRAM

                   DEFINE turnRight AS
                   BEGIN
                     turnLeft;
                     turnLeft;
                     turnLeft;
                   END

                   BEGINNING-OF-EXECUTION
                     ITERATE 3 TIMES
                     BEGIN
                       turnRight;
                         move
                       END
                       turnoff
                     END-OF-EXECUTION

                    END-OF-PROGRAM


      • Syntactic rules and patterns - conditionals and iteration
      • Defining new functions
      • Problem Decomposition
      • Logic and structure over calculation





========================================================================
Drill 1-0 a) Install stanfordkarel module by running the ff. in
             cmd or Anaconda prompt or Terminal.

                 pip install stanfordkarel

       (https://pypi.org/project/stanfordkarel/)

       b) Issue help() on stanfordkarel module for documentation
       and familiarize Karel commands.

       c) Run a simple Karel program where Karel moves forward 3 times.
========================================================================
'''

from karelcraft.karelcraft import *

# def main():
#   '''
#   Entry point for execution
#   '''
#   move()
#   move()
#   move()
#   move()
#   move()
#   move()
#   move()
#   print(facing_west())


# if __name__=="__main__":
#   run_karel_program()





r'''
               _          _    _
              / \    ___ | |_ (_)  ___   _ __   ___
             / _ \  / __|| __|| | / _ \ | '_ \ / __|
            / ___ \| (__ | |_ | || (_) || | | |\__ \
           /_/   \_\\___| \__||_| \___/ |_| |_||___/

                      BASIC FUNCTIONS

                      move() -> None

                      turn_left() -> None

                      pick_beeper() -> None

                      put_beeper() -> None

                      paint_corner(color: str) -> None



                             _  _  _    _                       _
       ___  ___   _ __    __| |(_)| |_ (_)  ___   _ __    __ _ | |
      / __|/ _ \ | '_ \  / _` || || __|| | / _ \ | '_ \  / _` || |
     | (__| (_) || | | || (_| || || |_ | || (_) || | | || (_| || |
      \___|\___/ |_| |_| \__,_||_| \__||_| \___/ |_| |_| \__,_||_|


   TEST                 OPPOSITE                    CHECKING


front_is_clear()    front_is_blocked()     Is there a wall in front of Karel?

left_is_clear()     left_is_blocked()      Is there a wall to Karel’s left?

right_is_clear()    right_is_blocked()     Is there a wall to Karel’s right?

beeper_present()    no_beeper_present()     Is there a beeper on this corner?

beepers_in_bag()    no_beepers_in_bag()    Any there beepers in Karel’s bag?







facing_north()      not_facing_north()     Is Karel facing north?

facing_east()       not_facing_east()      Is Karel facing east?

facing_south()      not_facing_south()     Is Karel facing south?

facing_west()       not_facing_west()      Is Karel facing west?

corner_color_is(color: str)         Is the color of corner (color: str)?



                        _ __  _   _  _ __
                       | '__|| | | || '_ \
                       | |   | |_| || | | |
                       |_|    \__,_||_| |_|

              run_karel_program(world_file: str = '') -> None



                                            __  __
              _ __ ___    ___ __   __ ___  / /  \ \
             | '_ ` _ \  / _ \\ \ / // _ \| |    | |
             | | | | | || (_) |\ V /|  __/| |    | |
             |_| |_| |_| \___/  \_/  \___|| |    | |
                                           \_\  /_/
                  move forward one square



  _                             _         __  _     __  __
 | |_  _   _  _ __  _ __       | |  ___  / _|| |_  / /  \ \
 | __|| | | || '__|| '_ \      | | / _ \| |_ | __|| |    | |
 | |_ | |_| || |   | | | |     | ||  __/|  _|| |_ | |    | |
  \__| \__,_||_|   |_| |_|_____|_| \___||_|   \__|| |    | |
                         |_____|                   \_\  /_/

               turn 90 degrees to the left




                _         _                                      __  __
  _ __   _   _ | |_      | |__    ___   ___  _ __    ___  _ __  / /  \ \
 | '_ \ | | | || __|     | '_ \  / _ \ / _ \| '_ \  / _ \| '__|| |    | |
 | |_) || |_| || |_      | |_) ||  __/|  __/| |_) ||  __/| |   | |    | |
 | .__/  \__,_| \__|_____|_.__/  \___| \___|| .__/  \___||_|   | |    | |
 |_|               |_____|                  |_|                 \_\  /_/

                  puts a beeper on the current square





         _        _                                                  __  __
  _ __  (_)  ___ | | __       _ __    ___   ___  _ __    ___  _ __  / /  \ \
 | '_ \ | | / __|| |/ /      | '_ \  / _ \ / _ \| '_ \  / _ \| '__|| |    | |
 | |_) || || (__ |   <       | |_) ||  __/|  __/| |_) ||  __/| |   | |    | |
 | .__/ |_| \___||_|\_\_____ | .__/  \___| \___|| .__/  \___||_|   | |    | |
 |_|                  |_____||_|                |_|                 \_\  /_/

                picks up a beeper from the current square




========================================================================
Drill 1-1 a) Write a Karel helper function to make Karel turn right.
          e.g. turn_right()

          b) Write a Karel helper function to make Karel turn around.
          e.g. turn_around()

          Note: This new functions extends the set of operation the
          robot can perform
========================================================================
'''


def turn_right():
  '''
  Makes Karel turn right
  '''
  turn_left()
  turn_left()
  turn_left()

def turn_around():
  '''
  Makes Karel turn around
  '''
  turn_left()
  turn_left()

# def main():
#   '''
#   Main program
#   '''
#   turn_right()
#   turn_left()
#   move()
#   turn_around()
#   turn_right()

# if __name__ == "__main__":
#   run_karel_program()



r'''                                       _  _  _    _
  _ __   _ __  ___   ___  ___   _ __    __| |(_)| |_ (_)  ___   _ __
 | '_ \ | '__|/ _ \ / __|/ _ \ | '_ \  / _` || || __|| | / _ \ | '_ \
 | |_) || |  |  __/| (__| (_) || | | || (_| || || |_ | || (_) || | | |
 | .__/ |_|   \___| \___|\___/ |_| |_| \__,_||_| \__||_| \___/ |_| |_|
 |_|
              what is true about the inputs to a function
                   to guarantee expected behavior

              or assumed true at the start of a method

        e.g.
                  • Karel starts at (1,1) facing East
                  • the world is rectangular and,
                  • there are no walls other than the outer border





                     _                          _  _  _    _
  _ __    ___   ___ | |_  ___  ___   _ __    __| |(_)| |_ (_)  ___   _ __
 | '_ \  / _ \ / __|| __|/ __|/ _ \ | '_ \  / _` || || __|| | / _ \ | '_ \
 | |_) || (_) |\__ \| |_| (__| (_) || | | || (_| || || |_ | || (_) || | | |
 | .__/  \___/ |___/ \__|\___|\___/ |_| |_| \__,_||_| \__||_| \___/ |_| |_|
 |_|
              what must always be true after the execution
                   of a function or block of code

              or promised to be true at the end of a method

        e.g.
                  • the world will be full of beepers
                  • Karel's final position will not important
                  • Karel may face in any direction




========================================================================
Drill 1-2 Write a Karel helper function to put beepers in the row
          applicable to *any* Karel world size.
          What are the preconditions and postconditions?
========================================================================
'''


def put_beeper_line():
  '''
  Pre: Karel at initial state (1,1) and facing East with infinite beepers
  Post: Beepers will completely fill a certain row
  '''
  while front_is_clear():
    put_beeper()
    move()
  put_beeper()

# def main():
#   put_beeper_line()


# if __name__ == "__main__":
#   run_karel_program()







r'''
        _
     __| |  ___   ___  ___   _ __ ___   _ __    ___   ___   ___
    / _` | / _ \ / __|/ _ \ | '_ ` _ \ | '_ \  / _ \ / __| / _ \
   | (_| ||  __/| (__| (_) || | | | | || |_) || (_) |\__ \|  __/
    \__,_| \___| \___|\___/ |_| |_| |_|| .__/  \___/ |___/ \___|
                                       |_|
              organizing a program as a number of parts

                e.g. the main() should be clutter-free



                   ____   ___    ___   ____
                  / ___| / _ \  / _ \ |  _ \
                 | |  _ | | | || | | || | | |
                 | |_| || |_| || |_| || |_| |
                  \____| \___/  \___/ |____/
                          PROGRAM

              • Simple and understandable parts
              • Meaningful function names and variables

========================================================================
Drill 1-3 Write a Karel helper function to solve the collect newspaper
          karel problem. Make Karel walk to the door of its house, pick
          up the newspaper (beeper), and then return to its initial
          position in the upper left corner of the house.
          What are the preconditions and postconditions?
========================================================================
'''


# YOUR CODE HERE

def go_to_door():
  '''
  pre: Karel at initial position
  post: Karel at the position of newspaper
  '''
  move()
  move()
  turn_right()
  move()
  turn_left()
  move()

def pick_newspaper():
  '''
  pre: Karel at beeper position with beeper present
  post:Karel at beeper position without the beeper in the corner
  '''
  pick_beeper()

def go_back_to_house():
  '''
  pre: Karel at beeper position without the beeper in the corner
  post: Karel is back to initial position
  '''
  turn_around()
  move()
  move()
  move()
  turn_right()
  move()
  turn_right()


# def main():
#   '''
#   pre: Initial Karel position in the house with newspaper outside the door
#   post: Karel already picked the newspaper and back to initial position
#   '''
#   go_to_door()
#   pick_newspaper()
#   go_back_to_house()



# if __name__ == '__main__':
#   run_karel_program('collect_newspaper_karel')








r'''
========================================================================
Drill 1-4 Write a Karel helper function to install beepers in the
          perimeter of the word. The solution should be able to solve
          any world size with least 2x2.
          Note: Do not repeat beeper installation.
          What are the preconditions and postconditions?
========================================================================
'''


def install_beepers():
  '''
  pre: Initial Karel satate at (1,1) facing east (empty world)
  post: The perimeter is filled with beepers
  '''
  while front_is_clear() and no_beeper_present():
    put_beeper()
    move()
    if front_is_blocked():
      turn_left()
  put_beeper()


# def main():
#   install_beepers()


# if __name__ == "__main__":
#   run_karel_program()





r'''
========================================================================
Drill 1-5 Write a Karel helper function to paint the perimeter 'Green'.
          What are the preconditions and postconditions?
========================================================================

                _         _
  _ __    __ _ (_) _ __  | |_       ___  ___   _ __  _ __    ___  _ __
 | '_ \  / _` || || '_ \ | __|     / __|/ _ \ | '__|| '_ \  / _ \| '__|
 | |_) || (_| || || | | || |_     | (__| (_) || |   | | | ||  __/| |
 | .__/  \__,_||_||_| |_| \__|_____\___|\___/ |_|   |_| |_| \___||_|
 |_|                         |_____|
'''



def paint_perimeter():
  '''
  pre: Initial Karel satate at (1,1) facing east (empty world)
  post: The perimeter is filled with beepers
  '''
  while front_is_clear() and not color_present():
    paint_corner('green')
    move()
    if front_is_blocked():
      turn_left()



# def main():
#   paint_perimeter()


# if __name__ == "__main__":
#   run_karel_program()




r'''
========================================================================
Drill 1-6 Write a Karel helper function to create an ascending staircase
          pattern of beepers. You can use a counter variable.
          What are the preconditions and postconditions?
========================================================================
'''

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



# def main():
#   staircase()


# if __name__ == "__main__":
#   run_karel_program()







r'''
========================================================================
Drill 1-7 Write a Karel helper function to create an ascending staircase
          pattern of colors. You can use a counter variable.
          What are the preconditions and postconditions?

Karel Colors:

colors = ["Red","Black","Cyan","Dark Gray", \
    "Gray", "Green", "Light Gray", "Magenta", \
    "Orange", "Pink", "White", "Blue","Yellow",
]
========================================================================
'''
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
  # colors = ["Red","Black","Cyan","Dark Gray", \
  #   "Gray", "Green", "Light Gray", "Magenta", \
  #   "Orange", "Pink",  "Blue","Yellow", # "White",
  # ]
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


# def main():
#   color_staircase()


# if __name__ == "__main__":
#   run_karel_program()




r'''
========================================================================
Drill 1-8 Write a Karel helper function to create an descending staircase
          pattern of beepers. You can use a counter variable.
          What are the preconditions and postconditions?
========================================================================
'''

# YOUR CODE HERE










r'''
========================================================================
Drill 1-8 Write a Karel helper function to create an descending staircase
          pattern of colors. You can use a counter variable.
          What are the preconditions and postconditions?
========================================================================
'''

# YOUR CODE HERE











r'''
========================================================================
Drill 1-9 Write a Karel helper function to create a pyramid pattern
          of colors. You can use variables.
          What are the preconditions and postconditions?
========================================================================
'''

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


# def main():
#   pyramid()


# if __name__ == "__main__":
#   run_karel_program()








r'''
========================================================================
Drill 1-10 Write a Karel program to create a random color pattern
          for any world size. No variables allowed.
          What are the preconditions and postconditions?
========================================================================
'''

# YOUR CODE HERE
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


# def main():
#   random_coloring()


# if __name__ == "__main__":
#   run_karel_program()







r'''
========================================================================
Drill 1-11 Write a Karel program to create rectangular layers of color.
          Note: World should be at least 2x2.
          What are the preconditions and postconditions?
========================================================================
'''

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

# def main():
#   rainbow_layers()


# if __name__ == "__main__":
#   run_karel_program()





r'''
========================================================================
Drill 1-12 Write a Karel program to create a random blocks
          for any world size. No variables allowed.
          What are the preconditions and postconditions?
========================================================================
'''

# YOUR CODE HERE
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

def random_blocks():
  if front_is_blocked():
    handle_column_world()
  else:
    handle_bigger_worlds()


# def main():
#   random_blocks()


# if __name__ == "__main__":
#   run_karel_program()
