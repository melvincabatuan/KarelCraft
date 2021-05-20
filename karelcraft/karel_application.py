"""
This file is the main object running the KarelCraft application.

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
from time import sleep
from typing import Callable
from ursina import *

from karelcraft.entities.world import World
from karelcraft.entities.karel import Karel, StudentCode
from karelcraft.entities.voxel import Voxel

from karelcraft.constants import TITLE, MAP_SIZE, WAIT_TIME

class App(Ursina):
    def __init__(self, code_file: Path) -> None:
        super().__init__()
        self.karel = Karel()
        self.speed = WAIT_TIME    # Wait per step
        self.setup_code(code_file)
        EditorCamera()
        self.set_3d()
        self.setup_textures()
        self.setup_lights()
        self.setup_window()
        self.init_prompt()
        self.setup_buttons()

    def setup_window(self) -> None:
        window.title = 'Running ' + self.student_code.module_name + '.py'
        window.color = color.black
        # window.render_mode = 'colliders' # Debugging
        # window.render_mode = 'normals'
        # window.render_mode = 'wireframe'
        # window.icon  = 'icon.png'
        # window.fullscreen = True
        window.borderless = False
        window.exit_button.visible = False
        window.fps_counter.enabled = False

    def setup_code(self, code_file) -> None:
        self.student_code = StudentCode(code_file)
        self.student_code.inject_namespace(self.karel)
        self.inject_decorator_namespace()

    def setup_textures(self) -> None:
        self.grass_texture = load_texture('assets/grass_block.png') # Ursina-Panda3D loader
        self.stone_texture = load_texture('assets/stone_block.png')
        self.brick_texture = load_texture('assets/brick_block.png')
        self.dirt_texture  = load_texture('assets/dirt_block.png')
        self.lava_texture  = load_texture('assets/lava_block.png')
        self.block_texture = self.grass_texture # default
        self.texture_name = 'grass'

    def setup_lights(self) -> None:
        Light(type='ambient', color=(0.6, 0.6, 0.6, 1))
        Light(type='directional', color=(0.6, 0.6, 0.6, 1), direction=(1, 1, 1))

    def handle_view(self) -> None:
        if self.view_button.value[0] == '3D':
            self.set_3d()
        if self.view_button.value[0] == '2D':
            self.set_2d()

    def setup_buttons(self) -> None:
        self.view_button = ButtonGroup(('2D', '3D'), min_selection = 1, \
            x = -0.8, y = -0.1, \
            default='3D', selected_color=color.green)
        self.view_button.on_value_changed = self.handle_view

    def init_prompt(self) -> None:
        Text(TITLE, position=window.center + Vec2(-0.14, 0.48), scale = 2)
        self.prompt = Text(f'Position : {self.karel.grid_position}; Direction: {self.karel.facing_to()}',
        position = window.center + Vec2(-0.16, -0.42),
        scale = 1)

    def update_prompt(self, agent_action) -> None:
        self.prompt.text = f'''      \t {agent_action}
        Position @ {self.karel.grid_position()} ==> {self.karel.facing_to()}
        '''

    def set_3d(self) -> None:
        camera.position = (MAP_SIZE // 2, -1.5*MAP_SIZE, -1.4*MAP_SIZE)
        camera.rotation_x = -55

    def set_2d(self) -> None:
        camera.rotation_x = 0
        camera.position   = (MAP_SIZE // 2, MAP_SIZE // 2, -3*MAP_SIZE)

    def input(self, key) -> None:
        if key == '2':
            self.set_2d()
        elif key == '3':
            self.set_3d()
        elif key == 'w' or key == 'a' or key == 's' or key == 'd' \
          or key == 'arrow_up' or key == 'arrow_down' \
          or key == 'arrow_left' or key == 'arrow_right':
            # Manual Movement
            self.karel.user_move(key)
            self.update_prompt('move()')
        elif key == '=':
            print("Make faster...")
            self.speed -= 0.05
        elif key == '-':
            print("Make slower...")
            self.speed += 0.05
        elif key == '4':
            self.texture_name = 'grass'
            self.block_texture = self.grass_texture
        elif key == '5':
            self.texture_name = 'stone'
            self.block_texture = self.stone_texture
        elif key == '6':
            self.texture_name = 'brick'
            self.block_texture = self.brick_texture
        elif key == '7':
            self.texture_name = 'dirt'
            self.block_texture = self.dirt_texture
        elif key == '8':
            self.texture_name = 'lava'
            self.block_texture = self.lava_texture
        elif key == 'escape':
            print("Manual mode: press wasd or arrow keys to move")
            sys.exit() # Manual mode

        super().input(key)

    def karel_action_decorator(
        self, karel_fn: Callable[..., None]
        ) -> Callable[..., None]:
        def wrapper() -> None:
            # execute Karel function
            karel_fn()
            agent_action = karel_fn.__name__+'()'
            # show prompt to user
            self.update_prompt(agent_action)
            # manual step Panda3D loop
            taskMgr.step()
            # delay by specified amount
            sleep(self.speed)
        return wrapper


    def corner_action_decorator(
        self, karel_fn: Callable[..., None]
        ) -> Callable[..., None]:
        def wrapper(key: str) -> None:
            # execute Karel function
            karel_fn(key)
            agent_action =  karel_fn.__name__+f'("{key}")'
            # show prompt to user
            self.update_prompt(agent_action)
            # manual step Panda3D loop
            taskMgr.step()
            # delay by specified amount
            sleep(self.speed)
        return wrapper

    def block_action_decorator(
        self, karel_fn: Callable[..., None]
        ) -> Callable[..., None]:
        def wrapper() -> None:
            # execute Karel function
            karel_fn(self.block_texture) # send texture to Karel
            agent_action = karel_fn.__name__+'() => ' + self.texture_name
            # show prompt to user
            self.update_prompt(agent_action)
            # manual step Panda3D loop
            taskMgr.step()
            # delay by specified amount
            sleep(self.speed)
        return wrapper

    def inject_decorator_namespace(self) -> None:
        """
        This function associates the generic commands in student code
        to KarelCraft functions. (Credits: stanford.karel module)
        """
        self.student_code.mod.turn_left = self.karel_action_decorator(
            self.karel.turn_left
        )
        self.student_code.mod.move = self.karel_action_decorator(
            self.karel.move
        )
        self.student_code.mod.put_beeper = self.karel_action_decorator(
            self.karel.put_beeper
        )
        self.student_code.mod.pick_beeper = self.karel_action_decorator(
            self.karel.pick_beeper
        )
        self.student_code.mod.paint_corner = self.corner_action_decorator(
            self.karel.paint_corner
        )
        self.student_code.mod.put_block    = self.block_action_decorator(
            self.karel.put_block
        )

    def run_program(self) -> None:
        try:
           self.student_code.mod.main()
           window.title = 'Manual mode: Use WASD or Arrow keys to control agent'
           base.win.requestProperties(window)
        except Exception as e:
            print(e)
            print("Karel Error", "Karel Crashed!")
        finally:
            self.run() # run the app for wasd/arrows exploration
            return 0   # PyOS_InputHook expects an integer
