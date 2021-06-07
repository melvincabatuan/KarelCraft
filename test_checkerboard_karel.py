from karelcraft.karelcraft import *
import random

# MODE = 'beeper'
# MODE, COLOR = 'paint', 'cyan'
MODE = 'block'

TEXTURES = ('grass', 'stone', 'brick', 'dirt', 'lava', 'rose',
            'dlsu', 'diamond', 'emerald', 'gold', 'obsidian',
            'leaves', 'sand', 'wood', 'stonebrick', 'sponge', 'snow')


def get_color():
    '''
    Returns a random color
    '''
    colors = ["red", "black", "cyan", "white",
              "smoke", "green", "light_gray", "gray",
              "dark_gray", "black", "magenta",
              "orange", "pink",  "blue", "yellow", "lime",
              "turquoise", "azure", "violet", "brown",
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
