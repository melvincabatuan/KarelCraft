from karelcraft.karelcraft import *

def turn_right():
    turn_left()
    turn_left()
    turn_left()


def main():
    # put_beeper()
    put_block()
    count = 1
    while front_is_clear():
        move()
        # put_beeper()
        put_block()
        count += 1

    if front_is_blocked():

        while count > 0:
            turn_left()
            if front_is_clear():
                move()
                turn_left()
                count -= 2
                install = count
                while front_is_clear() and install > 0:
                    move()
                    # put_beeper()
                    put_block()
                    install -= 1

            turn_right()
            if front_is_clear():
                move()
                turn_right()
                count -= 2
                install = count
                while front_is_clear() and install > 0:
                    move()
                    # put_beeper()
                    put_block()
                    install -= 1

            # exit 1 block world
            if front_is_blocked():
                break




if __name__ == "__main__":
    run_karel_program()
