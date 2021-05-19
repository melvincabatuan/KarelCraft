from karelcraft.karelcraft import *

def main():
    """ Your code goes here! """
    while front_is_clear():
        put_block()
        # put_beeper()
        # paint_corner('greegrid_position(n')
        move()

        if front_is_blocked():
            turn_left()

        if block_present():
            print("Breaking...")
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
'''
