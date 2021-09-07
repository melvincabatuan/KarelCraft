# Author: MKC

from karelcraft.karelcraft import *
from enum import Enum

MODE = 'beeper'
# MODE, COLOR = 'paint', 'blue'
# MODE = 'block'


def turn_around():
    turn_left()
    turn_left()


def turn_right():
    turn_around()
    turn_left()


def install(mode):
    if mode == 'paint':
        if no_color_present():
            paint_corner(COLOR)
    elif mode == 'block':
        if no_block_present():
            put_block()
    else:  # beeper is default
        if no_beepers_present():
            put_beeper()


def destroy(mode):
    if mode == 'paint':
        remove_paint()
    elif mode == 'block':
        destroy_block()
    else:
        pick_beeper()


def create_objects():
    while front_is_clear():
        install(MODE)
        move()
        if front_is_blocked():
            turn_left()
        if beeper_present() or color_present() or block_present():
            break


def destroy_objects():
    while beeper_present() or color_present() or block_present():
        if front_is_blocked():
            turn_right()
        destroy(MODE)
        move()


def main():
    """ Your code goes here! """
    create_objects()
    turn_around()
    destroy_objects()
    destroy(MODE)  # test karel exceptions for all objects


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
