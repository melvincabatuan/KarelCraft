# -*- coding: utf-8 -*-
"""
Created on Thu Sep  9 05:09:58 2021

@author: ECE
"""

from karelcraft.karelcraft import *

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

def put_block_line():
    '''
    Pre: Karel at initial state (1,1) and facing East with infinite beepers
    Post: Beepers will completely fill a certain row
    '''
    while front_is_clear():
        put_block('dlsu')
        move()
    put_block('dlsu')


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
        put_block_line()
        # put_beeper_line()
        turn_around()
        go_to_wall()
        go_to_next_step(step)
        step += 1

    # put_beeper_line() # handles fencepost error
    put_block_line()


def main():
    staircase()


if __name__ == "__main__":
    run_karel_program()