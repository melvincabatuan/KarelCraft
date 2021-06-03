from ursina import *
import importlib.util
from pathlib import Path

from karelcraft.utils.helpers import vec2tup, INFINITY, KarelException
from karelcraft.utils.direction import Direction
from karelcraft.entities.world import World

class Karel(Button):

    def __init__(self, world_file: str) -> None:
        super().__init__(
        parent   = scene,
        color    = color.white66,
        model    = 'assets/block', #'sphere',
        texture  = 'assets/karel_block',
        rotation = Vec3(90,90,90),
        scale = 0.48,
        )
        self.directions = {'a': Direction.WEST,
                           'd': Direction.EAST,
                           'w': Direction.NORTH,
                           's': Direction.SOUTH,
                    'arrow_up': Direction.NORTH,
                  'arrow_down': Direction.SOUTH,
                  'arrow_left': Direction.WEST,
                 'arrow_right': Direction.EAST,
                 }
        self.world_file = world_file
        self.init_params()

    def init_params(self):
        self.world     = World(self.world_file)
        self.position  = Vec3(self.world.loader.start_location + (-0.5,))
        self.direction = self.world.loader.start_direction
        self.face2direction()
        self.num_beepers = self.world.loader.start_beeper_count

    def facing_to(self) -> str:
        return self.direction.name

    def user_action(self, key) -> tuple:
        if self.direction != self.directions[key]:
            self.direction = self.directions[key]
            self.face2direction()
            return ('turn_left()', self.world.is_inside(self.position))
        else:
            is_valid_move = self.direction_is_clear(self.direction)
            self.position += self.direction.value
            self.position = self.world.top_position(self.position)
            return ('move()', is_valid_move)

    def move(self) -> None:
        if self.front_is_blocked():
            raise KarelException(
                self.position,
                self.facing_to(),
                'move()',
                "ERROR: Karel attempted to move(), but its front was not clear!",
            )
        self.position += self.direction.value
        self.position = self.world.top_position(self.position) # depth

    def facing_east(self) -> bool:
        return self.direction.name == 'EAST'

    def not_facing_east(self) -> bool:
        return not self.facing_east()

    def facing_north(self) -> bool:
        return self.direction.name == 'NORTH'

    def not_facing_north(self) -> bool:
        return not facing_north()

    def facing_west(self) -> bool:
        return self.direction.name == 'WEST'

    def not_facing_west(self) -> bool:
        return not self.facing_west()

    def facing_south(self) -> bool:
        return self.direction.name == 'SOUTH'

    def not_facing_south(self) -> bool:
        return not self.facing_south()

    def face2direction(self) -> None:
        if self.direction.name == 'SOUTH':
            self.rotation_x = 180
        elif self.direction.name == 'NORTH':
            self.rotation_x = 360
        elif self.direction.name == 'WEST':
            self.rotation_x = 270
        else: # 'EAST'
            self.rotation_x = 90
        # while Direction.angle(self.direction) != Direction.angle(new_direction):
        #     self.rotation_x -= 90
        #     self.direction = Direction.rotate90(self.direction)


    def turn_left(self) -> None:
        self.direction = Direction.rotate90(self.direction)
        self.face2direction()
        self.position = self.world.top_position(self.position) # depth

    def direction_is_clear(self, direction) -> bool:
        is_wall = self.world.wall_exists(self.position, direction)
        new_position = self.position + direction.value
        is_wall += self.world.wall_exists(new_position, Direction.opposite(direction))
        return self.world.is_inside(new_position) and not is_wall

    def front_is_clear(self) -> bool:
        return self.direction_is_clear(self.direction)

    def front_is_blocked(self) -> bool:
        return not self.front_is_clear()

    def left_is_clear(self) -> bool:
        return self.direction_is_clear(Direction.rotate90(self.direction))

    def left_is_blocked(self) -> bool:
        return not self.left_is_clear()

    def right_is_clear(self) -> bool:
        return self.direction_is_clear(Direction.rotate90(self.direction, 'counterclockwise'))

    def right_is_blocked(self) -> bool:
        return not self.right_is_clear()

    def put_beeper(self) -> int:
        if self.num_beepers == 0:
            raise KarelException(
                self.position,
                self.facing_to(),
                'put_beeper()',
                "ERROR: Karel attempted to put_beeper(), but it had none left in its bag.",
            )
        if self.num_beepers != INFINITY:
            self.num_beepers -= 1
        key = vec2tup(self.position)[:2]
        self.world.add_beeper(key)
        self.position = self.world.top_position(self.position)
        return len(self.world.beepers.get(key,[]))

    def pick_beeper(self) -> int:
        if self.no_beeper_present():
            raise KarelException(
                self.position,
                self.facing_to(),
                'pick_beeper()',
                "ERROR: Karel attempted to pick_beeper(), but it does not exist!",
            )
        if self.num_beepers != INFINITY:
            self.num_beepers += 1

        beepers_in_stack = self.world.remove_beeper(self.position)
        self.position = self.world.top_position(self.position)
        return beepers_in_stack

    def beeper_present(self) -> bool:
        key = vec2tup(self.position)[:2]
        return len(self.world.beepers.get(key, []))

    def beepers_present(self) -> bool:
        return self.beeper_present()

    def no_beeper_present(self) -> bool:
        return not self.beeper_present()

    def no_beepers_present(self) -> bool:
        return self.no_beeper_present()

    def beepers_in_bag(self) -> bool:
        self.num_beepers != 0

    def no_beepers_in_bag(self) -> bool:
        return self.num_beepers == 0

    def item_position(self):
        return Vec3(self.position.x, self.position.y, 0)

    def paint_corner(self, color_str: str) -> None:
        self.world.paint_corner(self.item_position(), color_str)

    def corner_color_is(self, color: str) -> bool:
        return self.world.corner_color(self.item_position()) == color

    def color_present(self) -> bool:
        return self.world.paints.get(tuple(self.item_position()), False)

    def no_color_present(self) -> bool:
        return not self.color_present()

    def put_block(self, texture) -> None:
        key = vec2tup(self.position)[:2]
        idx_in_stack = len(self.world.voxels.get(key,[]))
        self.position = Vec3(self.position.x, self.position.y,-idx_in_stack*self.world.voxel_offset_z - 0.5)
        block_pos = Vec3(self.position.x, self.position.y, self.position.z + 0.5)
        self.world.add_voxel(block_pos, texture)
        return idx_in_stack + 1

    def block_present(self) -> bool:
        key = vec2tup(self.position)[:2]
        return bool(len(self.world.voxels.get(key, [])))

    def no_block_present(self) -> bool:
        return not self.block_present()

    def destroy_block(self) -> None:
        if self.block_present():
            self.world.remove_voxel(tuple(self.item_position()))
            self.position = self.world.top_position(self.position)
        else:
            raise KarelException(
                self.item_position(),
                self.facing_to(),
                'destroy_block()',
                "ERROR: Karel attempted to destroy_block(), but it does not exist!",
            )

    def remove_paint(self) -> None:
        if self.color_present():
            self.world.remove_color(tuple(self.item_position()))
        else:
            raise KarelException(
                self.position,
                self.facing_to(),
                'remove_paint()',
                "ERROR: Karel attempted to remove_paint(), but it does not exist!",
            )

    def animate_movement(self) -> None:
        particle = Entity(model='sphere',
            position=self.position,
            scale=0.0,
            texture='circle',
            add_to_scene_entities=False)
        particle.animate_scale(0.8, 1.2,
            curve=curve.out_expo)
        particle.animate_color(color.yellow,
            duration=.3,
            curve=curve.out_expo)
        destroy(particle, delay=.2)


class StudentCode:
    """
    This process extracts a module from an arbitary file that contains student code.
    https://stackoverflow.com/questions/67631/how-to-import-a-module-given-the-full-path
    (Credits: stanford.karel module)
    """
    def __init__(self, code_file: Path) -> None:
        if not code_file.is_file():
            raise FileNotFoundError(f"{code_file} could not be found.")

        self.module_name = code_file.stem
        spec = importlib.util.spec_from_file_location(
            self.module_name, code_file.resolve()
        )
        try:
            self.mod = importlib.util.module_from_spec(spec)
            spec.loader.exec_module(self.mod)  # type: ignore
        except SyntaxError as e:
            print(f"Syntax Error: {e}")
            print("\n".join(tb.format_exc(limit=0).split("\n")[1:]))
            sys.exit()

        # Do not proceed if the student has not defined a main function.
        if not hasattr(self.mod, "main"):
            print("Couldn't find the main() function. Are you sure you have one?")
            sys.exit()

    def __repr__(self) -> str:
        return inspect.getsource(self.mod)

    def inject_namespace(self, karel: Karel) -> None:
        """
        This function associates the generic commands the student code to
        specific commands in KarelCraft. (Credits: stanford.karel module)
        """
        functions_to_override = [
            "move",
            "turn_left",
            "pick_beeper",
            "put_beeper",
            "put_block",
            "destroy_block",
            "facing_north",
            "facing_south",
            "facing_east",
            "facing_west",
            "not_facing_north",
            "not_facing_south",
            "not_facing_east",
            "not_facing_west",
            "front_is_clear",
            "beeper_present",
            "beepers_present",
            "no_beeper_present",
            "no_beepers_present",
            "block_present",
            "no_block_present",
            "beepers_in_bag",
            "no_beepers_in_bag",
            "front_is_blocked",
            "left_is_blocked",
            "left_is_clear",
            "right_is_blocked",
            "right_is_clear",
            "paint_corner",
            "remove_paint",
            "corner_color_is",
            "color_present",
            "no_color_present",
        ]
        for func in functions_to_override:
            setattr(self.mod, func, getattr(karel, func))

