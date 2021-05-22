from karelcraft.karelcraft import *


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

def go_to_upper_base(width):
    if width % 2 == 0:
        install_a_beeper()
    look("north", facing_north)
    move_forward(width//2)
    look("east", facing_east)
    move_to_wall()

# DRY Principle: Don't Repeat Yourself
def install_triangle(width, is_bottom = True):
    for i in range(width, 0, -2):
        for _ in range(i):
            look("west", facing_west)
            install_a_beeper()
            move()
        install_a_beeper()
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
