"""
This file is the main object running the KarelCraft application.

Author : Melvin Cabatuan
ThanksTo: pokepetter (Ursina)
         Nicholas Bowman, Kylie Jue, Tyler Yep (stanfordkarel module)
         clear-code-projects (Minecraft-in-Python)
         StanislavPetrovV
License: MIT
Version: 1.0.0
Date of Creation: 5/17/2021
"""

import sys
import webbrowser
import random
from pathlib import Path
from time import sleep
from typing import Callable
from ursina import *

from karelcraft.entities.world import World
from karelcraft.entities.karel import Karel, StudentCode
from karelcraft.entities.voxel import Voxel
from karelcraft.entities.cog_menu import CogMenu
from karelcraft.utils.helpers import vec2tup, KarelException

TITLE = "KarelCraft"
TEXTURE_NAMES = ('grass','stone','brick','dirt','lava', 'rose', \
      'dlsu', 'diamond', 'emerald', 'gold', 'obsidian', \
      'leaves', 'sand', 'wood', 'stonebrick', 'sponge', 'snow')


class App(Ursina):

    def __init__(self,
        code_file: Path,
        world_file: str,
        development_mode=False,
        ) -> None:
        super().__init__()
        self.karel = Karel(world_file.split('.')[0]) # remove extension
        self.setup_code(code_file)
        self.run_code = False
        EditorCamera(rotation_speed = 100 )
        self.set_3d()
        self.setup_textures()
        self.setup_sound()
        self.setup_lights()
        self.setup_window()
        self.init_prompt()
        self.setup_controls()
        self.setup_menu()

    def setup_window(self) -> None:
        window.title = TITLE
        window.color = color.black
        # window.render_mode = 'colliders' # Debugging
        # window.render_mode = 'normals'
        # window.render_mode = 'wireframe'
        # window.fullscreen = True
        window.borderless = False
        window.exit_button.visible = False
        window.fps_counter.enabled = False

    def setup_code(self, code_file) -> None:
        self.student_code = StudentCode(code_file)
        self.student_code.inject_namespace(self.karel)
        self.inject_decorator_namespace()

    def setup_textures(self) -> None:
        self.textures = {
            'grass' : load_texture('assets/grass_block.png'),
            'stone' : load_texture('assets/stone_block.png'),
            'brick' : load_texture('assets/brick_block.png'),
            'dirt'  : load_texture('assets/dirt_block.png'),
            'lava'  : load_texture('assets/lava_block.png'),
            'rose'  : load_texture('assets/rose_block.png'),
            'dlsu'  : load_texture('assets/dlsu_block.png'),
         'diamond'  : load_texture('assets/diamond_block.png'),
         'emerald'  : load_texture('assets/emerald_block.png'),
         'gold'     : load_texture('assets/gold_block.png'),
         'obsidian' : load_texture('assets/obsidian_block.png'),
         'leaves'   : load_texture('assets/leaves_block.png'),
         'sand'     : load_texture('assets/sand_block.png'),
         'wood'     : load_texture('assets/wood_block.png'),
     'stonebrick'   : load_texture('assets/stonebrick_block.png'),
         'sponge'   : load_texture('assets/sponge_block.png'),
         'snow'     : load_texture('assets/snow_block.png'),
        }
        self.texture_name = TEXTURE_NAMES[0]     # default
        self.block_texture = self.textures[self.texture_name]

    def setup_sound(self):
        self.move_sound = Audio('assets/move.mp3', autoplay = False) # loop = True,

    def setup_lights(self) -> None:
        Light(type='ambient', color=(0.6, 0.6, 0.6, 1))
        Light(type='directional', color=(0.6, 0.6, 0.6, 1), direction=(1, 1, 1))

    def handle_view(self) -> None:
        if self.view_button.value[0] == '3D':
            self.set_3d()
        if self.view_button.value[0] == '2D':
            self.set_2d()

    def handle_speed(self) -> None:
        self.karel.world.speed = self.speed_slider.value

    def setup_menu(self) -> None:
        window.cog_menu.enabled = False
        self.menu = CogMenu({
        'Karelcraft Repo' : Func(webbrowser.open, 'https://github.com/melvincabatuan/KarelCraft'),
        'Change Texture <gray>[1 to 7]<default>'  : self.set_texture,
        'Change Render Mode <gray>[F10]<default>' : window.next_render_mode,
        'Camera 3D View <gray>[Page Up]<default>' : self.set_3d,
        'Camera 2D View <gray>[Page Down]<default>' : self.set_2d,
        })
        self.menu.on_click = Func(setattr, self.menu, 'enabled', False)

    def setup_controls(self) -> None:
        # Run button:
        self.run_button = Button(position=(-0.75, 0.28),
            text='Run',
            color = color.gray,
            pressed_color = color.green,
            parent = camera.ui,
            eternal=True,
            scale = 0.062,
            )
        self.run_button.text_entity.scale = 0.7
        self.run_button.on_click = self.set_run_code
        self.run_button.tooltip = Tooltip('Run Student Code')

        # Reset button:
        self.reset_button = Button(position=(-0.75, 0.2),
            text='Reset',
            color = color.gray,
            pressed_color = color.green,
            parent = camera.ui,
            eternal=True,
            scale = 0.062,
            )
        self.reset_button.text_entity.scale = 0.7
        self.reset_button.on_click = self.reset
        self.reset_button.tooltip = Tooltip('Reset the world')

        # Camera button:
        self.view_button = ButtonGroup(('2D', '3D'),
            min_selection = 1,
            x = -0.8, y = 0.13,
            default='3D',
            selected_color=color.green,
            parent = camera.ui,
            eternal=True,
            )
        self.view_button.on_value_changed = self.handle_view
        self.view_button.scale *= 0.85

        # Slider
        self.speed_slider = ThinSlider(0.0, 1.0,
            default = self.karel.world.speed,
            step = 0.02,
            text='Speed',
            dynamic=True,
            position=(-0.75, -0.4),
            vertical = True,
            parent = camera.ui,
            eternal=True,
            )
        self.speed_slider.scale *= 0.85
        self.speed_slider.bg.color = color.white66
        self.speed_slider.knob.color = color.green
        self.speed_slider.on_value_changed = self.handle_speed

    def init_prompt(self) -> None:
        Text(TITLE,
            position=window.center + Vec2(-0.14, 0.48),
            scale = 2,
            parent = camera.ui,
            eternal=True,
            )
        self.prompt = Text(f'Position : {vec2tup(self.karel.position)}; Direction: {self.karel.facing_to()}',
        position = window.center + Vec2(-0.36, -0.43),
        scale = 1,
        parent = camera.ui
        )

    def update_prompt(self, agent_action, error_message = None) -> None:
        position = self.karel.position
        position.z = abs(position.z) # correct Ursina coordinate (-) at top
        msg =  f'''           \t {agent_action}
        \t Position @ {vec2tup(position)} ==> {self.karel.facing_to()}
        '''
        self.prompt.color = color.white
        if error_message:
            msg = error_message + '\n' + '\t' + msg.split('\n')[1]
            self.prompt.color = color.red
        self.prompt.text = msg

    def set_3d(self) -> None:
        span = self.karel.world.scale.x
        camera.position = (span // 2, -1.5*span, -1.4*span)
        camera.rotation_x = -55

    def set_2d(self) -> None:
        camera.rotation_x = 0
        span = self.karel.world.scale.x
        camera.position   = (span // 2, span // 2, -3*span)

    def set_texture(self, key=None) -> None:
        if key is None:
            key = random.randint(1,5)
            self.texture_name  = TEXTURE_NAMES[key-1]
        else:
            self.texture_name  = TEXTURE_NAMES[int(key)-1]
        self.block_texture = self.textures[self.texture_name]

    def set_run_code(self):
        self.run_code = True
        self.run_button.disabled = True

    def reset(self):
        to_destroy = [e for e in scene.entities \
            if e.name == 'voxel' or e.name == 'paint' \
            or e.name == 'beeper']
        for d in to_destroy:
            try:
                destroy(d)
            except Exception as e:
                print('failed to destroy entity', e)
        self.karel.init_params()
        self.karel.world.speed = self.speed_slider.value

    def input(self, key) -> None:
        if key == 'w' or key == 'a' or key == 's' or key == 'd' \
          or key == 'arrow_up' or key == 'arrow_down' \
          or key == 'arrow_left' or key == 'arrow_right':
            # Manual Movement
            action, is_valid = self.karel.user_action(key)
            msg    = '\tturn_left()'
            error_msg = ''
            if action == 'move()':
                msg    = '\tmove()'
            if not is_valid:
                error_msg = '\t\t  ERROR: Invalid move()!'
            self.update_prompt(msg, error_msg)
            self.move_sound.play()
        elif key == '=':
            print("Make faster...")
            self.karel.world.speed = min(self.karel.world.speed + 0.05, 1.0)
        elif key == '-':
            print("Make slower...")
            self.karel.world.speed = max(self.karel.world.speed - 0.05, 0.0)
        elif key.isdigit() and '1' <= key <= '8':
             self.set_texture(key)
        elif key == 'page_down':
            self.set_3d()
        elif key == 'page_up':
            self.set_2d()
        elif key == 'r': # run student code
            self.set_run_code()
        elif key == 'c': # clear
            # self.clear_objects()
            self.karel.world.clear_objects()
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
            self.update_prompt('\t' + agent_action)
            # action sound
            self.move_sound.play()
            # manual step Panda3D loop
            taskMgr.step()
            # delay by specified amount
            sleep(1 - self.karel.world.speed)
        return wrapper

    def corner_action_decorator(
        self, karel_fn: Callable[..., None]
        ) -> Callable[..., None]:
        def wrapper(color: str) -> None:
            # execute Karel function
            karel_fn(color)
            agent_action =  karel_fn.__name__+f'("{color}")'
            # show prompt to user
            self.update_prompt(agent_action)
            # manual step Panda3D loop
            taskMgr.step()
            # delay by specified amount
            sleep(1 - self.karel.world.speed)
        return wrapper

    def beeper_action_decorator(
        self, karel_fn: Callable[..., None]
        ) -> Callable[..., None]:
        def wrapper() -> None:
            # execute Karel function
            num_beepers = karel_fn()
            agent_action =  karel_fn.__name__ + f'() => ' + str(num_beepers)
            # show prompt to user
            self.update_prompt(agent_action)
            # manual step Panda3D loop
            taskMgr.step()
            # delay by specified amount
            sleep(1 - self.karel.world.speed)
        return wrapper

    def block_action_decorator(
        self, karel_fn: Callable[..., None]
        ) -> Callable[..., None]:
        def wrapper(block_texture: str = TEXTURE_NAMES[0]) -> None:
            #set texture if given
            self.block_texture = self.textures[block_texture]
            # execute Karel function
            karel_fn(self.block_texture) # send texture to Karel
            agent_action = karel_fn.__name__+'() => ' + self.texture_name
            # show prompt to user
            self.update_prompt(agent_action)
            # manual step Panda3D loop
            taskMgr.step()
            # delay by specified amount
            sleep(1 - self.karel.world.speed)
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
        self.student_code.mod.put_beeper = self.beeper_action_decorator(
            self.karel.put_beeper
        )
        self.student_code.mod.pick_beeper = self.beeper_action_decorator(
            self.karel.pick_beeper
        )
        self.student_code.mod.paint_corner = self.corner_action_decorator(
            self.karel.paint_corner
        )
        self.student_code.mod.put_block    = self.block_action_decorator(
            self.karel.put_block
        )
        self.student_code.mod.destroy_block = self.karel_action_decorator(
            self.karel.destroy_block
        )
        self.student_code.mod.remove_paint  = self.karel_action_decorator(
            self.karel.remove_paint
        )

    def debug_message(self, text, position=window.center, origin=(-.5,.5), scale=2, duration=4) -> None:
        debug_txt = Text(text=text, position=position, origin=origin, scale=scale, color=color.red)
        destroy(debug_txt, delay=duration)

    def run_student_code(self) -> None:
        window.title = 'Running ' + self.student_code.module_name + '.py'
        # base.win.requestProperties(window)
        try:
            self.move_sound.play()
            self.student_code.mod.main()
        except KarelException as e:
            self.update_prompt(e.action, e.message)
        except Exception as e:
            print(e)
        except SystemExit: # ignore traceback on exit
            pass
        self.run_button.disabled = False


    def run_program(self) -> None:
        try:
            # Update the title
            window.title = self.student_code.module_name + \
                ' : Manual mode - Use WASD or Arrow keys to control agent'
            window.center_on_screen()
            base.win.requestProperties(window)
            # self.run() # run the app for wasd/arrows exploration
                         # not run() does not return, thus, use step() instead
            while True:
                taskMgr.step()
                if self.run_code:
                    self.run_student_code()
                    self.run_code = False
        except SystemExit: # ignore traceback on exit
            pass
        except Exception as e:
            print(e)



    def finalizeExit(self):
        """
        Called by `userExit()` to quit the application.
        """
        base.graphicsEngine.removeAllWindows()
        if self.win is not None:
            print("Exiting app, bye!")
            self.closeWindow(self.win)
            self.win = None
        self.destroy()
        sys.exit()
