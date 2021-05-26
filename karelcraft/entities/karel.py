from ursina import *
import importlib.util
from pathlib import Path

from karelcraft.utils.helpers import vec2tup
from karelcraft.utils.constants import MAP_SIZE, NWSE_MAP, NEXT_NWSE,\
            NEXT_NWSE_CCW, INIT_BEEPERS, NORTH, SOUTH, EAST, WEST, INFINITY
from karelcraft.entities.world import World

class Karel(Button):

    Z_OFFSET = 0

    def __init__(self) -> None:
        super().__init__(
        position =  Vec3(0, 0,-0.5),
        parent   = scene,
        color    = color.white,
        model    = 'assets/block', #'sphere',
        texture  = 'assets/karel_block',
        rotation = Vec3(90,90,90),
        scale = 0.5,
        )
        self.world      = World(MAP_SIZE)
        self.directions = {'a': Vec3(WEST),  'd': Vec3(EAST), \
                           'w': Vec3(NORTH), 's': Vec3(SOUTH), \
            'arrow_up': Vec3(NORTH), 'arrow_down': Vec3(SOUTH), \
          'arrow_left': Vec3(WEST), 'arrow_right': Vec3(EAST)}
        self.direction = Vec3(EAST)
        # self.setup_collider()
        self.num_beepers = INIT_BEEPERS

    def setup_collider(self) -> None:
        axis = BoxCollider(self,
            size=self.scale * Vec3(0.1, 0.1, 10),
            )
        axis.show()
        self.collider = axis

    def facing_to(self) -> str:
        return NWSE_MAP[tuple(self.direction)]

    def user_move(self, key) -> bool:
        self.direction = self.directions[key]
        self.face2direction()
        self.position += self.direction
        return self.world.is_inside(self.position)

    def move(self) -> None:
        if self.front_is_blocked():
            raise KarelException(
                self.position,
                self.facing_to(),
                'move()',
                "ERROR: Karel attempted to move(), but its front was not clear!",
            )
        self.position += self.direction

    def facing_east(self) -> bool:
        return self.direction == Vec3(EAST)

    def not_facing_east(self) -> bool:
        return not self.facing_east()

    def facing_north(self) -> bool:
        return self.direction == Vec3(NORTH)

    def not_facing_north(self) -> bool:
        return not facing_north()

    def facing_west(self) -> bool:
        return self.direction == Vec3(WEST)

    def not_facing_west(self) -> bool:
        return not self.facing_west()

    def facing_south(self) -> bool:
        return self.direction == Vec3(SOUTH)

    def not_facing_south(self) -> bool:
        return not self.facing_south()

    def face2direction(self) -> None:
        if self.direction == Vec3(SOUTH):
            self.rotation_x = 180
        elif self.direction == Vec3(NORTH):
            self.rotation_x = 0
        elif self.direction == Vec3(WEST):
            self.rotation_x = 270
        else:
            self.rotation_x = 90


    def turn_left(self) -> None:
        self.direction = Vec3(NEXT_NWSE[tuple(self.direction)])
        self.face2direction()

    def direction_is_clear(self, direction) -> bool:
        new_position = self.position + direction
        return self.world.is_inside(new_position)

    def front_is_clear(self) -> bool:
        return self.direction_is_clear(self.direction)

    def front_is_blocked(self) -> bool:
        return not self.front_is_clear()

    def left_is_clear(self) -> bool:
        return self.direction_is_clear(Vec3(NEXT_NWSE[tuple(self.direction)]))

    def left_is_blocked(self) -> bool:
        return not self.left_is_clear()

    def right_is_clear(self) -> bool:
        return self.direction_is_clear(Vec3(NEXT_NWSE_CCW[tuple(self.direction)]))

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

        beeper_pos = Vec3(self.position.x, self.position.y, self.Z_OFFSET)
        return self.world.add_beeper(beeper_pos)

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

        return self.world.remove_beeper(self.position)

    def beeper_present(self) -> bool:
        key = vec2tup(self.position)[:2]
        return len(self.world.beepers.get(key, []))
        # hit_info = self.intersects() # Ursina collider presents inconsistent results
        # if hit_info.hit:
        #     return hit_info.entity.type == 'Beeper'
        # return False

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
        return Vec3(self.position.x, self.position.y, self.Z_OFFSET)

    def paint_corner(self, key: str) -> None:
        self.world.paint_corner(self.item_position(), key)

    def corner_color_is(self, color: str) -> bool:
        return self.world.corner_color(self.item_position()) == color

    def color_present(self) -> bool:
        return self.world.paints.get(tuple(self.item_position()), False)
        # hit_info = self.intersects()
        # if hit_info.hit:
        #     return hit_info.entity.type == 'ColorPaint'
        # return False

    def no_color_present(self) -> bool:
        return not self.color_present()

    def put_block(self, texture) -> None:
        self.world.add_voxel(self.item_position(), texture)

    def block_present(self) -> bool:
        return self.world.voxels.get(tuple(self.item_position()), False)
        # hit_info = self.intersects()
        # if hit_info.hit:
        #     return hit_info.entity.type == 'Voxel'
        # return False

    def no_block_present(self) -> bool:
        return not self.block_present()

    def destroy_block(self) -> None:
        if self.block_present():
            self.world.remove_voxel(tuple(self.position))
        else:
            raise KarelException(
                self.position,
                self.facing_to(),
                'destroy_block()',
                "ERROR: Karel attempted to destroy_block(), but it does not exist!",
            )

    def remove_paint(self) -> None:
        if self.color_present():
            self.world.remove_color(tuple(self.position))
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


class KarelException(Exception):
    def __init__(self, position: tuple,
        direction: str,
        action: str,
        message: str) -> None:
        super().__init__()
        self.position  = position
        self.direction = direction
        self.action    = action
        self.message   = message

    def __str__(self) -> str:
        return (
            f"Karel crashed while on position {self.position}, "
            f"facing {self.direction}\nInvalid action: {self.message}"
        )
