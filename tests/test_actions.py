# -*- coding: utf-8 -*-
"""
Created on Thu Sep  9 04:34:29 2021

@author: ECE
"""

from karelcraft.karelcraft import *

def main():
    '''
    Write your code solution here;     
    '''
    move()
    turn_left()
    put_beeper()
    pick_beeper()
    put_block('diamond')
    destroy_block()
    paint_corner('green')
    remove_paint()


if __name__ == "__main__":
    run_karel_program()

