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
Last Modified: 9/11/2021
"""
from ursina import *
from karelcraft.entities.karel import Karel
from karelcraft.entities.cog_menu import CogMenu
from karelcraft.entities.radial_menu import RadialMenu, RadialMenuButton
from karelcraft.entities.file_browser_save import FileBrowserSave
from karelcraft.entities.dropdown_menu import DropdownMenu, DropdownMenuButton
from karelcraft.utils.helpers import vec2tup, vec2key, KarelException
from karelcraft.utils.student_code import StudentCode
from karelcraft.utils.world_loader import COLOR_LIST, TEXTURE_LIST

import sys
import webbrowser
import random
from pathlib import Path
from time import sleep
from typing import Callable

TITLE = 'KarelCraft'
BLOCKS_PATH = 'assets/blocks/'
REPO_PATH = 'https://github.com/melvincabatuan/KarelCraft'
application.asset_folder = Path(__file__).resolve().parent / 'assets'


class App(Ursina):

    def __init__(self, code_file: Path, world_file: str, development_mode=False) -> None:
        super().__init__()
        self.setup_texture()
        self.karel = Karel(world_file, self.textures)
        self.world = self.karel.world
        self.code_file = code_file
        self.setup_window()
        self.setup_code()
        self.setup_controls()
        self.init_prompt()
        self.setup_menu()
        self.setup_sound_lights_cam()
        self.create_mode = 'voxel'  # default
        self.color_name = random.choice(COLOR_LIST)

    def setup_texture(self):
        default_texture_path = Path(__file__).resolve().parent / BLOCKS_PATH
        self.textures = {
            texture_path.stem.split('_')[0]: load_texture(str(texture_path.stem))
            for texture_path in default_texture_path.glob("*.png")
        }
        self.texture_names = list(self.textures.keys())
        self.texture_name = random.choice(self.texture_names)
        self.block_texture = self.textures.get(self.texture_name, 'grass')

    def setup_window(self) -> None:
        window.title = TITLE
        window.color = color.black
        window.borderless = False
        window.exit_button.visible = False
        window.fps_counter.enabled = False

    def setup_code(self) -> None:
        self.student_code = StudentCode(self.code_file)
        self.student_code.inject_namespace(self.karel)
        self.inject_decorator_namespace()
        self.run_code = False

    def load_audio(self, filepath: str) -> audio.Audio:
        sound = Audio(sound_file_name=None, loop=False, autoplay=False)
        unix_path = filepath.replace('lib', 'Lib')
        unix_path = unix_path.replace('C:', '/c')
        sound.clip = base.loader.loadSfx(unix_path)
        return sound

    def setup_sound_lights_cam(self):
        MOVE_SOUND_PATH = Path(__file__).absolute().parent.as_posix() + '/assets/sounds/move.mp3'
        DESTROY_SOUND_PATH = Path(__file__).absolute().parent.as_posix() + \
            '/assets/sounds/destroy.wav'
        self.move_sound = self.load_audio(MOVE_SOUND_PATH)
        self.destroy_sound = self.load_audio(DESTROY_SOUND_PATH)

        Light(type='ambient', color=(0.6, 0.6, 0.6, 1))
        Light(type='directional', color=(0.6, 0.6, 0.6, 1), direction=(1, 1, 1))
        EditorCamera(rotation_speed=25)  # lessen angle adjustment
        self.set_3d()

    def handle_view(self) -> None:
        if self.view_button.value[0] == '3D':
            self.set_3d()
        else:
            self.set_2d()

    def handle_speed(self) -> None:
        self.world.speed = self.speed_slider.value

    def setup_menu(self) -> None:
        window.cog_menu.enabled = False
        self.menu = CogMenu({
            'Save World State <gray>[ctrl+s]<default>': self.save_world,
            'Change Texture <gray>[0 to 9]<default>': self.set_texture,
            'Change Render Mode <gray>[F10]<default>': window.next_render_mode,
            'Camera 3D View <gray>[P/Page Up]<default>': self.set_3d,
            'Camera 2D View <gray>[P/Page Down]<default>': self.set_2d,
            'Select color': self.enable_color_menu,
            'Karelcraft Repo': Func(webbrowser.open, REPO_PATH),
        })
        self.menu.on_click = Func(setattr, self.menu, 'enabled', False)
        self.menu.eternal = True

    def setup_controls(self) -> None:
        # Run button:
        self.run_button = Button(
            model='circle',
            position=(-0.75, 0.36),
            text='Run',
            color=color.gray,
            pressed_color=color.green,
            parent=camera.ui,
            eternal=True,
            scale=0.064,
        )
        self.run_button.text_entity.scale = 0.7
        self.run_button.on_click = self.set_run_code
        self.run_button.tooltip = Tooltip('Run Student Code')

        # Stop button:
        self.stop_button = Button(
            model='circle',
            position=(-0.75, 0.28),
            text='Stop',
            color=color.gray,
            pressed_color=color.red,
            parent=camera.ui,
            eternal=True,
            scale=0.064,
        )
        self.stop_button.text_entity.scale = 0.7
        self.stop_button.on_click = self.stop_code
        self.stop_button.tooltip = Tooltip('Stop Student Code')

        # Reset button:
        self.reset_button = Button(
            model='circle',
            position=(-0.75, 0.20),
            text='Reset',
            color=color.gray,
            pressed_color=color.yellow,
            parent=camera.ui,
            eternal=True,
            scale=0.064,
        )
        self.reset_button.text_entity.scale = 0.7
        self.reset_button.on_click = self.reset
        self.reset_button.tooltip = Tooltip('Reset the world')

        # Camera button:
        self.view_button = ButtonGroup(('2D', '3D'),
                                       min_selection=1,
                                       x=-0.8, y=0.13,
                                       default='3D',
                                       selected_color=color.green,
                                       parent=camera.ui,
                                       eternal=True,
                                       )
        self.view_button.on_value_changed = self.handle_view
        self.view_button.scale *= 0.85

        # Slider
        self.speed_slider = ThinSlider(0.0, 1.0,
                                       default=self.world.speed,
                                       step=0.02,
                                       text='Speed',
                                       dynamic=True,
                                       position=(-0.75, -0.4),
                                       vertical=True,
                                       parent=camera.ui,
                                       eternal=True,
                                       )
        self.speed_slider.scale *= 0.85
        self.speed_slider.bg.color = color.white66
        self.speed_slider.knob.color = color.green
        self.speed_slider.on_value_changed = self.handle_speed

        # World selector
        button_list = []
        for w in self.world.world_list:
            drop_button = DropdownMenuButton(w)
            drop_button.on_click = lambda w=w: self.load_world(w)
            button_list.append(drop_button)

        DropdownMenu('Load World',
                     buttons=button_list,
                     position=(0.52, 0.48),
                     eternal=True,
                     )

        # Color selector
        radial_list = []
        for k in COLOR_LIST:
            color_button = RadialMenuButton(scale=.4, color=color.colors[k])
            color_button.on_click = lambda k=k: self.change_color(k)
            radial_list.append(color_button)

        self.color_selector = RadialMenu(
            buttons=(radial_list),
            enabled=False,
            eternal=True,
        )

    def enable_color_menu(self):
        self.color_selector.enabled = True

    def change_color(self, color_name):
        self.color_name = color_name
        self.color_selector.enabled = False

    def init_prompt(self) -> None:
        Text(TITLE,
             position=window.center + Vec2(-0.14, 0.48),
             scale=2,
             parent=camera.ui,
             eternal=True,
             )
        msg = f'Position : {vec2tup(self.karel.position)}; Direction: {self.karel.direction.name}'
        self.prompt = Text(msg,
                           position=window.center + Vec2(-0.36, -0.43),
                           scale=1,
                           parent=camera.ui
                           )

    def update_prompt(self, agent_action, error_message=None) -> None:
        position = self.karel.position
        position.z = abs(position.z)  # correct Ursina coordinate (-) at top
        msg = f'''           \t {agent_action}
        \t Position @ {vec2tup(position)} ==> {self.karel.direction.name}
        '''
        self.prompt.color = color.white
        if error_message:
            msg = error_message + '\n' + '\t' + msg.split('\n')[1]
            self.prompt.color = color.red
        self.prompt.text = msg

    def set_3d(self) -> None:
        span = self.world.get_maxside()
        x_center, y_center = self.world.get_center()
        y_pos = min(-1.6 * span, -12.7)
        self.z_pos = min(-1.4 * span, -12)
        camera.position = (x_center, y_pos, self.z_pos)
        camera.rotation_x = -55
        self.view_button.select(self.view_button.buttons[1])

    def set_2d(self) -> None:
        camera.rotation_x = 0
        span = self.world.get_maxside()
        self.z_pos = min(-3 * span, -10)
        x_center, y_center = self.world.get_center()
        camera.position = (x_center, y_center, self.z_pos)
        self.view_button.select(self.view_button.buttons[0])

    def set_texture(self, key=None) -> None:
        if key is None:
            self.texture_name = random.choice(self.texture_names)
        else:
            self.texture_name = self.texture_names[int(key) - 1]
        # self.block_texture = self.textures[self.texture_name]

    def set_run_code(self) -> None:
        self.run_code = True
        self.run_button.disabled = True

    def stop_code(self) -> None:
        self.run_code = False
        self.stop_button.disabled = True

    def reset(self) -> None:
        to_destroy = [e for e in scene.entities
                      if e.name == 'voxel' or e.name == 'paint'
                      or e.name == 'beeper']
        for d in to_destroy:
            try:
                destroy(d)
            except Exception as e:
                print('failed to destroy entity', e)
        self.karel.init_params()
        self.world = self.karel.world
        self.world.speed = self.speed_slider.value

    def clear_objects(self) -> None:
        to_destroy = [e for e in scene.entities
                      if e.name == 'voxel' or e.name == 'paint'
                      or e.name == 'beeper' or e.name == 'wall']
        for d in to_destroy:
            try:
                destroy(d)
            except Exception as e:
                print('failed to destroy entity', e)

    def load_world(self, world_file: str) -> None:
        '''
        Loads a world, i.e. world_file, from ./karelcraft/worlds/ directory
        Destroy existing entities except UI, then, recreate them
        '''
        to_destroy = [e for e in scene.entities
                      if e.name == 'voxel' or e.name == 'paint' or
                      e.name == 'beeper' or e.name == 'wall' or
                      e.name == 'karel' or e.name == 'world']
        for d in to_destroy:
            try:
                destroy(d)
            except Exception as e:
                print('failed to destroy entity', e)
        del self.karel
        self.karel = Karel(world_file, self.textures)
        self.world = self.karel.world
        self.setup_code()
        self.world.speed = self.speed_slider.value
        self.set_3d()
        msg = f'Position : {vec2tup(self.karel.position)}; Direction: {self.karel.direction.name}'
        self.update_prompt(msg)

    def save_world(self) -> None:
        wp = FileBrowserSave(file_type='.w')
        try:
            wp.path = Path('./karelcraft/worlds/')
            wp.data = self.get_world_state()
        except Exception:  # use current dir instead
            print(f"Can't find the directory {wp.path}. Using current directory...")
            wp.data = self.get_world_state()

    def get_world_state(self) -> str:
        world_state = f"Karel: {vec2key(self.karel.position)}; "
        world_state += f"{self.karel.direction.name.title()}\n"
        world_state += f"Dimension: ({self.world.size.col}, {self.world.size.row})\n"
        beeper_output = (
            self.karel.num_beepers
            if self.karel.start_beeper_count >= 0
            else "INFINITY"
        )
        world_state += f"BeeperBag: {beeper_output}\n"

        for key in sorted(self.world.stacks.keys()):
            if self.world.all_beepers(key):
                world_state += f"Beeper: ({key[0]}, {key[1]}); {self.world.count_beepers(key)}\n"
            elif self.world.all_same_blocks(key):
                texture_name = self.world.top_in_stack(key).texture_name
                world_state += f"Block: ({key[0]}, {key[1]}); {texture_name}; "
                world_state += f"{self.world.count_blocks(key)}\n"
            elif self.world.all_colors(key):
                color_name = self.world.corner_color((key[0], key[1], 0))
                world_state += f"Color: ({key[0]}, {key[1]}); {color_name}\n"
            elif self.world.stacks.get(key, []):
                world_state += f"Stack: ({key[0]}, {key[1]}); {self.world.stack_string(key)}\n"

        for wall in sorted(self.world.walls):
            world_state += f"Wall: ({wall.col}, {wall.row}); {wall.direction.name.title()}\n"

        return world_state

    def destroy_item(self) -> None:
        '''
        Destroys the item - voxel, beeper, paint - hovered by the mouse
        Logic: You can only destroy the top of the stack
        '''
        if to_destroy := mouse.hovered_entity:
            pos_to_destroy = to_destroy.position
            self.destroy_sound.play()
            if to_destroy == self.world.top_in_stack(pos_to_destroy):
                if to_destroy.name == 'voxel':
                    self.world.remove_voxel(pos_to_destroy)
                elif to_destroy.name == 'beeper':
                    self.world.remove_beeper(pos_to_destroy)
                elif to_destroy.name == 'paint':
                    self.world.remove_color(pos_to_destroy)
                if vec2key(pos_to_destroy) == vec2key(self.karel.position):
                    self.karel.update_z()

    def create_item(self) -> None:
        '''
        Create an item in agent's position
        '''
        if self.create_mode == 'voxel':
            self.karel.put_block(self.texture_name)
            agent_action = 'put_block() => ' + self.texture_name
            self.update_prompt(agent_action)
        elif self.create_mode == 'paint_color':
            self.karel.paint_corner(self.color_name)
            agent_action = 'paint_corner() => ' + self.color_name
            # self.world.paint_corner(self.karel.position, self.color_name)
        elif self.create_mode == 'beeper':
            self.world.add_beeper(self.karel.position)
            agent_action = 'add_beeper() => '
        self.karel.update_z()

    def input(self, key) -> None:
        '''
        Handles user input:
            - Agent movement: wasd or arrows keys
            - Increase / Decrease speed: = / -
            - Choose texture: 1 to 9
            - Change camera: Page Up/ Page Down
            - Run code: r
            - Clear objects: c
            - Emergency stop: escape
            - Save world state: ctrl + s
            - Destroy objects: left mouse or mouse1
        '''
        if key == 'w' or key == 'a' or key == 's' or key == 'd':
                # or key == 'arrow_up' or key == 'arrow_down' \
                # or key == 'arrow_left' or key == 'arrow_right':
            # Manual Movement
            action, is_valid = self.karel.user_action(key)
            msg = '\tturn_left()'
            error_msg = ''
            if action == 'move()':
                msg = '\tmove()'
            if not is_valid:
                error_msg = '\t\t  ERROR: Invalid move()!'
            self.update_prompt(msg, error_msg)
            self.move_sound.play()
        elif key == '=':
            print("Make faster...")
            self.world.speed = min(self.world.speed + 0.05, 1.0)
        elif key == '-':
            print("Make slower...")
            self.world.speed = max(self.world.speed - 0.05, 0.0)
        elif key.isdigit() and '1' <= key <= '9':
            self.set_texture(key)
        elif key == 'page_down':
            self.set_3d()
        elif key == 'page_up':
            self.set_2d()
        elif key == 'b':  # beeper
            self.create_mode = 'beeper'
        elif key == 'backspace':  # clear
            self.clear_objects()
        elif key == 'c':  # paint color
            self.create_mode = 'paint_color'
        elif key == 'r':  # run student code
            self.set_run_code()
        elif key == 'v':  # paint
            self.create_mode = 'voxel'
        elif key == 'z':  # zoom
            camera.rotation_x = 0
            x_center, y_center = self.world.get_center()
            self.z_pos += 5
            camera.position = (x_center, y_center, self.z_pos)
        elif key == 'x':  # zoom
            camera.rotation_x = 0
            x_center, y_center = self.world.get_center()
            self.z_pos -= 5
            camera.position = (x_center, y_center, self.z_pos)
        elif key == 'escape':
            print("Manual mode: press wasd or arrow keys to move")
            sys.exit()  # Manual mode
        elif key == 'control-s':
            self.save_world()
        elif key == 'mouse1':  # left click
            self.destroy_item()
        elif key == 'arrow_up':
            camera.rotation_x += 2
        elif key == 'arrow_down':
            camera.rotation_x -= 2
        elif key == 'arrow_right':
            camera.rotation_y -= 2
        elif key == 'arrow_left':
            camera.rotation_y += 2

        # elif key == 'mouse3':  # right click
        #     self.create_item()
        super().input(key)

    def end_frame(self, msg) -> None:
        self.update_prompt(msg)
        self.move_sound.play()
        taskMgr.step()  # manual step Panda3D loop
        sleep(1 - self.world.speed)  # delay by specified amount

    def karel_action_decorator(
        self, karel_fn: Callable[..., None]
    ) -> Callable[..., None]:
        def wrapper() -> None:
            if not self.run_code:
                sys.exit()
            karel_fn()  # execute Karel function
            self.end_frame('\t' + karel_fn.__name__ + '()')
        return wrapper

    def corner_action_decorator(
        self, karel_fn: Callable[..., None]
    ) -> Callable[..., None]:
        def wrapper(color: str = color.random_color()) -> None:
            karel_fn(color)
            self.end_frame(karel_fn.__name__ + f'("{color}")')
        return wrapper

    def beeper_action_decorator(
        self, karel_fn: Callable[..., None]
    ) -> Callable[..., None]:
        def wrapper() -> None:
            num_beepers = karel_fn()
            self.end_frame(karel_fn.__name__ + '() => ' + str(num_beepers))
        return wrapper

    def block_action_decorator(
        self, karel_fn: Callable[..., None]
    ) -> Callable[..., None]:
        def wrapper(block_texture: str = TEXTURE_LIST[0]) -> None:
            karel_fn(block_texture)
            self.end_frame(f'{karel_fn.__name__}() => {block_texture}')
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
        self.student_code.mod.put_block = self.block_action_decorator(
            self.karel.put_block
        )
        self.student_code.mod.destroy_block = self.karel_action_decorator(
            self.karel.destroy_block
        )
        self.student_code.mod.remove_paint = self.karel_action_decorator(
            self.karel.remove_paint
        )

    def run_student_code(self) -> None:
        window.title = 'Running ' + self.student_code.module_name + '.py'
        # base.win.requestProperties(window)
        self.stop_button.disabled = False
        try:
            self.move_sound.play()
            self.student_code.mod.main()
        except KarelException as e:
            self.update_prompt(e.action, e.message)
            self.run_code = False
            self.run_button.disabled = False
        except Exception as e:
            print(e)
        except SystemExit:  # ignore traceback on exit
            pass
        self.run_button.disabled = False

    def run_program(self) -> None:
        try:
            # Update the title
            window.title = self.student_code.module_name + \
                ' : Manual mode - Use WASD or Arrow keys to control agent'
            window.center_on_screen()
            base.win.requestProperties(window)

            while True:
                taskMgr.step()
                if self.run_code:
                    self.run_student_code()
                    self.run_code = False
        except SystemExit:  # ignore traceback on exit
            pass
        except Exception as e:
            print(e)

    def finalizeExit(self) -> None:
        """
        Called by `userExit()` to quit the application.
        """
        base.graphicsEngine.removeAllWindows()
        if self.win is not None:
            print("Exiting KarelCraft app, bye!")
            self.closeWindow(self.win)
            self.win = None
        self.destroy()
        sys.exit()
