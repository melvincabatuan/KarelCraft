from ursina import *

from karelcraft.utils.helpers import INFINITY, KarelException
from karelcraft.utils.direction import Direction
from karelcraft.entities.world import World
from karelcraft.utils.helpers import vec2key


# MODEL_PATH = str(Path(__file__).absolute().parent.parent / 'assets/block')
# TEXTURE_PATH = str(Path(__file__).absolute().parent.parent / 'assets/karel_block')

class Karel(Button):

    def __init__(self, world_file: str, textures: dict) -> None:
        super().__init__(
            parent=scene,
            color=color.white66,
            # model=MODEL_PATH,  # 'sphere',
            # texture=TEXTURE_PATH,
            model='block',
            texture='karel_block',
            rotation=Vec3(90, 90, 90),
            scale=0.48,
        )
        self.directions = {'a': Direction.WEST,
                           'd': Direction.EAST,
                           'w': Direction.NORTH,
                           's': Direction.SOUTH,
                           # 'arrow_up': Direction.NORTH,
                           # 'arrow_down': Direction.SOUTH,
                           # 'arrow_left': Direction.WEST,
                           # 'arrow_right': Direction.EAST,
                           }
        self.world_file = world_file
        self.textures = textures
        self.init_params()

    def init_params(self):
        self.world = World(self.world_file, self.textures)
        key = self.world.world_loader.start_location
        self.position = Vec3(key + (self.world.top_position(key)[-1],))
        self.direction = self.world.world_loader.start_direction
        self.face2direction()
        self.start_beeper_count = self.world.world_loader.start_beeper_count
        self.num_beepers = self.start_beeper_count

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
                self.direction.name,
                'move()',
                "ERROR attempt to move()",
            )
        self.position += self.direction.value
        self.position = self.world.top_position(self.position)  # depth

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
        else:  # 'EAST'
            self.rotation_x = 90

    def turn_left(self) -> None:
        self.direction = Direction.rotate90(self.direction)
        self.face2direction()
        self.position = self.world.top_position(self.position)  # depth

    def direction_is_clear(self, direction) -> bool:
        is_wall = self.world.wall_exists(self.position, direction)
        new_position = self.position + direction.value
        is_wall += self.world.wall_exists(new_position,
                                          Direction.opposite(direction))
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
        return self.direction_is_clear(
            Direction.rotate90(self.direction, 'counterclockwise')
        )

    def right_is_blocked(self) -> bool:
        return not self.right_is_clear()

    def put_beeper(self) -> int:
        if self.num_beepers == 0:
            raise KarelException(
                self.position,
                self.direction.name,
                'put_beeper()',
                "ERROR attempt to put_beeper(), (none left in bag)",
            )
        if self.num_beepers != INFINITY:
            self.num_beepers -= 1
        num_of_beepers = self.world.add_beeper(self.position)
        self.position = self.world.top_position(self.position)
        return num_of_beepers

    def pick_beeper(self) -> int:
        if self.no_beeper_present():
            raise KarelException(
                self.position,
                self.direction.name,
                'pick_beeper()',
                "ERROR attempt to pick_beeper()",
            )
        if self.num_beepers != INFINITY:
            self.num_beepers += 1

        beepers_in_stack = self.world.remove_beeper(self.position)
        self.position = self.world.top_position(self.position)
        return beepers_in_stack

    def beeper_present(self) -> bool:
        return bool(self.world.count_beepers(vec2key(self.position)))

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
        return bool(self.world.corner_color(self.item_position()))

    def no_color_present(self) -> bool:
        return not self.color_present()

    def put_block(self, texture_name) -> None:
        num_of_blocks = self.world.add_voxel(self.position, texture_name)
        self.update_z()
        return num_of_blocks

    def update_z(self) -> None:
        self.position = self.world.top_position(self.position)

    def block_present(self) -> bool:
        return bool(self.world.count_blocks(vec2key(self.position)))

    def no_block_present(self) -> bool:
        return not self.block_present()

    def destroy_block(self) -> None:
        if self.block_present():
            self.world.remove_voxel(self.position)
            self.position = self.world.top_position(self.position)
        else:
            raise KarelException(
                self.item_position(),
                self.direction.name,
                'destroy_block()',
                'ERROR attempted to destroy_block()',
            )

    def remove_paint(self) -> None:
        if self.color_present():
            self.world.remove_color(tuple(self.item_position()))
        else:
            raise KarelException(
                self.position,
                self.direction.name,
                'remove_paint()',
                'ERROR attempt to remove_paint()',
            )

    def get_position(self) -> None:
        return tuple(self.position)
