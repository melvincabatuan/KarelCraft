'''
This creates a 3D pyramid pattern of blocks.
@author: MKC
'''


from karelcraft.karelcraft import *
import random

TEXTURES = ('grass', 'stone', 'brick', 'dirt', 'lava', 'rose',
            'dlsu', 'diamond', 'emerald', 'gold', 'obsidian',
            'leaves', 'sand', 'wood', 'stonebrick', 'sponge', 'snow')


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
    run_karel_program('7x7')
