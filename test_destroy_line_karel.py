# Author: MKC

from karelcraft.karelcraft import *
from enum import Enum


class Mode(Enum):
    block = 1
    beeper = 2
    paint = 3


# Set the item to put in corner
# mode = Mode.beeper
# mode = Mode.paint
mode = Mode.block


def turn_around():
    turn_left()
    turn_left()


def main():
    """ Your code goes here! """
    while front_is_clear():
        if mode == Mode.block:
            put_block()
        elif mode == Mode.beeper:
            put_beeper()
        elif mode == Mode.paint:
            paint_corner('green')
        else:
            put_beeper()
        move()

    turn_around()
    move()

    while front_is_clear():
        if mode == Mode.block:
            destroy_block()
        elif mode == Mode.beeper:
            pick_beeper()
        elif mode == Mode.paint:
            remove_paint()

        move()

    # Test exceptions:
    if mode == Mode.block:
        destroy_block()
        destroy_block()  # Should return an exception

    elif mode == Mode.beeper:
        pick_beeper()
        pick_beeper()  # Should return an exception

    elif mode == Mode.paint:
        remove_paint()
        remove_paint()  # Should return an exception


'''
Note: Ursina collider presents inconsistent results
e.g. detection is ok at low speed x <= 0.8 but
doesn't detect if speed is greater.
'''


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
