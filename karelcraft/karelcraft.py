"""
This file defines the required functions and definitions
for a KarelCraft program. It must include the following:

from karelcraft.karelcraft import *

Author : Melvin Cabatuan
Credits: pokepetter (Ursina)
         Nicholas Bowman, Kylie Jue, Tyler Yep (stanfordkarel module)
         clear-code-projects (Minecraft-in-Python)
         StanislavPetrovV
License: MIT
Version: 1.0.0
Date of Creation: 5/17/2021
"""
import sys
from pathlib import Path
from karelcraft.karel_application import App
"""
The following function definitions are defined as stubs so that IDEs can recognize
the function definitions in student code. (Credits: stanford.karel module)
"""

def move() -> None:
    pass

def turn_left() -> None:
    pass

def put_beeper() -> None:
    pass

def put_block(block_texture: str) -> None:
    pass

def destroy_block() -> None:
    pass

def pick_beeper() -> None:
    pass

def front_is_clear() -> bool:
    pass

def front_is_blocked() -> bool:
    pass

def left_is_clear() -> bool:
    pass

def left_is_blocked() -> bool:
    pass

def right_is_clear() -> bool:
    pass

def right_is_blocked() -> bool:
    pass

def beeper_present() -> bool:
    pass

def beepers_present() -> bool:
    pass

def no_beeper_present() -> bool:
    pass

def no_beepers_present() -> bool:
    pass

def block_present() -> bool:
    pass

def no_block_present() -> bool:
    pass

def beepers_in_bag() -> bool:
    pass

def no_beepers_in_bag() -> bool:
    pass

def facing_north() -> bool:
    pass

def not_facing_north() -> bool:
    pass

def facing_east() -> bool:
    pass

def not_facing_east() -> bool:
    pass

def facing_west() -> bool:
    pass

def not_facing_west() -> bool:
    pass

def facing_south() -> bool:
    pass

def not_facing_south() -> bool:
    pass

def paint_corner(color: str) -> None:
    pass

def remove_paint() -> None:
    pass

def corner_color_is(color: str) -> bool:
    pass

def color_present() -> bool:
    pass

def no_color_present() -> bool:
    pass


def run_karel_program(world_file: str = "") -> None:
    student_filename = Path(sys.argv[0])
    app = App(student_filename)
    app.run_program()
