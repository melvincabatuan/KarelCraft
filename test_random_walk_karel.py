from karelcraft.karelcraft import *
import random

TEXTURES = ('grass', 'stone', 'brick', 'dirt', 'lava', 'rose',
            'dlsu', 'diamond', 'emerald', 'gold', 'obsidian',
            'leaves', 'sand', 'wood', 'stonebrick', 'sponge', 'snow'
            )

COLORS = ("red", "black", "cyan", "white",
          "smoke", "green", "light_gray", "gray",
          "dark_gray", "black", "magenta",
          "orange", "pink",  "blue", "yellow", "lime",
          "turquoise", "azure", "violet", "brown",
          "olive", "peach", "gold", "salmon"
          )

# rng = random.SystemRandom()
rng = random.Random()


def rand_turn():
    for _ in range(rng.randint(0, 3)):
        turn_left()


def rand_move():
    rand_turn()
    if front_is_clear():
        move()


def rand_create():
    option = rng.choice(('beeper', 'paint', 'voxel', ''))
    if option == 'beeper':
        put_beeper()
    elif option == 'paint':
        paint_corner(rng.choice(COLORS))
    elif option == 'voxel':
        put_block(rng.choice(TEXTURES))
    else:  # do nothing
        rand_move()


def rand_destroy():
    option = rng.choice(('beeper', 'paint', 'voxel', ''))
    if option == 'beeper' and beeper_present():
        pick_beeper()
    elif option == 'paint' and color_present():
        remove_paint()
    elif option == 'voxel' and block_present():
        destroy_block()
    else:  # do nothing
        rand_move()


def main():
    epochs = 1000
    for _ in range(epochs):
        action = rng.choice(('move', 'create', 'destroy', ''))
        if action == 'move':
            rand_move()
        elif action == 'create':
            rand_create()
        elif action == 'destroy':
            rand_destroy()
        else:
            rand_move()


if __name__ == "__main__":
    run_karel_program()
