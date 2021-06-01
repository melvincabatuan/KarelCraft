# Author: MKC

from karelcraft.karelcraft import *
from enum import Enum

class Mode(Enum):
    block  = 1
    beeper = 2
    paint  = 3

# Set the item to put in corner
# mode = Mode.beeper
# mode = Mode.paint
mode = Mode.block

def main():
    """ Your code goes here! """
    while front_is_clear():
        if mode == Mode.block:
            put_block('grass')
        elif mode == Mode.beeper:
            put_beeper()
        elif mode == Mode.paint:
            paint_corner('gold')
        else:
            put_beeper()

        move()

        if front_is_blocked():
            turn_left()

        if block_present() or beeper_present() or color_present():
            print("Perimeter done...")
            break

if __name__ == "__main__":
    run_karel_program()

'''
Available colors in Ursina:

white =         color(0, 0, 1)
smoke =         color(0, 0, 0.96)
light_gray =    color(0, 0, 0.75)
gray =          color(0, 0, 0.5)
dark_gray =     color(0, 0, 0.25)
black =         color(0, 0, 0)
red =           color(0, 1, 1)
yellow =        color(60, 1, 1)
lime =          color(90, 1, 1)
green =         color(120, 1, 1)
turquoise =     color(150, 1, 1)
cyan =          color(180, 1, 1)
azure =         color(210, 1, 1)
blue =          color(240, 1, 1)
violet =        color(270, 1, 1)
magenta =       color(300, 1, 1)
pink =          color(330, 1, 1)
brown =         rgb(165, 42, 42)
olive =         rgb(128, 128, 0)
peach =         rgb(255, 218, 185)
gold =          rgb(255, 215, 0)
salmon =        rgb(250, 128, 114)
...

'''
