from ursina import *
import importlib.util
from pathlib import Path

from karelcraft.constants import MAP_SIZE, EAST, WEST, NORTH, SOUTH
from karelcraft.entities.world import World

class Karel(Button):

    DIRECTION_MAP = {
        EAST:  'EAST',
        WEST:  'WEST',
        NORTH: 'NORTH',
        SOUTH: 'SOUTH'
    }

    NEXT_DIRECTION_MAP = {
            Vec3(NORTH): Vec3(WEST),
            Vec3(WEST): Vec3(SOUTH),
            Vec3(SOUTH): Vec3(EAST),
            Vec3(EAST): Vec3(NORTH),
    }

    NEXT_DIRECTION_MAP_RIGHT = {
            v: k for k, v in NEXT_DIRECTION_MAP.items()
    }

    INIT_POSITION = (1, 1, 0)
    POSITION_OFFSET = (0.5, 0.5, 0.5)
    Z_OFFSET = -0.01

    def __init__(self) -> None:
        super().__init__(
        position =  Vec3(0,0,0),
        model    = 'sphere',
        parent   = scene,
        color    = color.red #rgb(8,120,48) # GREEN
        )
        self.init_position()
        self.world      = World(MAP_SIZE)
        # self.parent     = self.world
        self.directions = {'a': Vec3(WEST),  'd': Vec3(EAST), \
                           'w': Vec3(NORTH), 's': Vec3(SOUTH), \
            'arrow_up': Vec3(NORTH), 'arrow_down': Vec3(SOUTH), \
          'arrow_left': Vec3(WEST), 'arrow_right': Vec3(EAST)}
        self.direction = Vec3(EAST)
        self.setup_collider()

    def init_position(self):
        self.position = Vec3(self.INIT_POSITION) - Vec3(self.POSITION_OFFSET)

    def setup_collider(self) -> None:
        axis = BoxCollider(self,
            # center=self.position + self.scale/2,
            size=self.scale * Vec3(0.1, 0.1, 10),
            )
        axis.show()
        self.collider = axis

    def facing_to(self) -> str:
        return self.DIRECTION_MAP[tuple(self.direction)]

    def grid_position(self) -> tuple:
        return self.world.grid_position(self.position)

    def user_move(self, key) -> bool:
        self.direction = self.directions[key]
        self.position += self.direction
        return self.world.is_inside(self.position)

    def move(self) -> None:
        if self.front_is_blocked():
            raise KarelException(
                self.grid_position(),
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

    def turn_left(self) -> None:
        self.direction = self.NEXT_DIRECTION_MAP[self.direction]

    def direction_is_clear(self, direction) -> bool:
        new_position = self.position + direction
        return self.world.is_inside(new_position)

    def front_is_clear(self) -> bool:
        return self.direction_is_clear(self.direction)

    def front_is_blocked(self) -> bool:
        return not self.front_is_clear()

    def left_is_clear(self) -> bool:
        return self.direction_is_clear( self.NEXT_DIRECTION_MAP[self.direction])

    def left_is_blocked(self) -> bool:
        return not self.left_is_clear()

    def right_is_clear(self) -> bool:
        return self.direction_is_clear( self.NEXT_DIRECTION_MAP_RIGHT[self.direction])

    def right_is_blocked(self) -> bool:
        return not self.right_is_clear()

    def put_beeper(self) -> None:
        beeper_pos = Vec3(self.position.x, self.position.y, self.Z_OFFSET)
        self.world.add_beeper(beeper_pos)

    def pick_beeper(self) -> None:
        if self.beeper_present():
            self.world.remove_beeper(self.position)
        else:
            print("Nothing to remove!") # TODO: raise Error

    def beeper_present(self) -> bool:
        hit_info = self.intersects()
        if hit_info.hit:
            return hit_info.entity.type == 'Beeper'
        return False

    def no_beeper_present(self) -> bool:
        return not self.beeper_present()

    def beepers_in_bag(self) -> bool:
        #TODO
        pass

    def no_beepers_in_bag(self) -> bool:
        #TODO
        pass

    def paint_corner(self, key: str) -> None:
        paint_pos = Vec3(self.position.x, self.position.y, self.Z_OFFSET)
        self.world.paint_corner(paint_pos, key)

    def corner_color_is(self, color: str) -> bool:
        return self.world.corner_color(self.position) == color

    def color_present(self) -> bool:
        hit_info = self.intersects()
        if hit_info.hit:
            return hit_info.entity.type == 'ColorPaint'
        return False

    def no_color_present(self) -> bool:
        return not self.color_present()

    def put_block(self, texture) -> None:
        block_pos = Vec3(self.position.x, self.position.y, self.Z_OFFSET)
        self.world.add_voxel(block_pos, texture)

    def block_present(self) -> bool:
        hit_info = self.intersects()
        if hit_info.hit:
            return hit_info.entity.type == 'Voxel'
        return False

    def no_block_present(self) -> bool:
        return not self.block_present()

    def destroy_block(self) -> None:
        if self.block_present():
            self.world.remove_voxel(self.position)
        else:
            print("Nothing to remove!") # TODO: raise Error

    def remove_paint(self) -> None:
        if self.color_present():
            self.world.remove_color(self.position)
        else:
            print("Nothing to remove!") # TODO: raise Error

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
            "no_beeper_present",
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
