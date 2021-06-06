from ursina import *
from karelcraft.entities.voxel import Voxel
from karelcraft.entities.beeper import Beeper
from karelcraft.entities.paint import Paint
from karelcraft.entities.wall import Wall
from karelcraft.utils.helpers import vec2tup, vec2key
from karelcraft.utils.world_loader import WorldLoader, COLOR_LIST, TEXTURE_LIST
from karelcraft.utils.direction import Direction
from collections import defaultdict
from typing import NamedTuple

class Size(NamedTuple):
    col: int
    row: int

class World(Entity):

    GROUND_OFFSET = -0.5
    BEEPER_OFFSET_Z = 0.04
    VOXEL_OFFSET_Z = 0.28

    def __init__(self, world_file: str, textures: dict) -> None:
        super().__init__(
            model    = 'quad',
            parent   = scene,
            color    = rgb(125, 125, 125),
        )
        self.world_loader = WorldLoader(world_file)
        self.textures = textures
        self.size   = Size(self.world_loader.columns, self.world_loader.rows)
        self.set_position((self.size.col/ 2, self.size.row/2, 0))
        self.scale = Vec3(self.size.col, self.size.row, 0)
        self.create_grid()
        self.position_correction()
        self.speed =  self.world_loader.init_speed
        self.world_list = self.world_loader.available_worlds
        self.stacks : dict[tuple[int, int], list]   = defaultdict(list)
        self.load_beepers()
        self.load_paints()
        self.load_walls()
        self.load_blocks()
        self.load_stacks()

    def position_correction(self):
        '''
        Offset used for centering the position to intersection,
        e.g. (0,0),(1,1), not (0.5, 0.5)
        '''
        self.world_position -= Vec3((0.5, 0.5, -0.01))

    def create_grid(self, height = -0.001):
        Entity(model = Grid(self.size.col, self.size.row, thickness=1.8),
            scale = 1,
            position = (self.origin.x, self.origin.y, height),
            color = color.white,
            parent = self
        )

    def load_beepers(self) -> None:
        for key, val in self.world_loader.beepers.items():
            for _ in range(val):
                self.add_beeper(key)

    def load_walls(self) -> None:
        self.walls = self.world_loader.walls
        for w in self.walls:
            wall_pos = Vec3(w.col, w.row, -1)
            wall_object = Wall(position = wall_pos, direction = w.direction)

    def load_paints(self) -> None:
        for key, paint in self.world_loader.corner_colors.items():
            paint_pos = Vec3(key[0], key[1], 0)
            self.paint_corner(paint_pos, paint)

    def load_blocks(self) -> None:
        for key, item in self.world_loader.blocks.items():
            block_pos = Vec3(key[0], key[1], 0)
            for _ in range(item[1]):
                self.add_voxel(block_pos, self.textures[item[0]] )

    def load_stacks(self) -> None:
        for key, stack_string in self.world_loader.stack_strings.items():
            for item in stack_string.split():
                initial = item[0]
                if initial == 'b':
                    self.add_beeper(key)
                elif initial == 'p':
                    paint_pos = Vec3(key[0], key[1], 0)
                    self.paint_corner(paint_pos, COLOR_LIST[int(item[1:])])
                elif initial == 'v':
                    block_pos = Vec3(key[0], key[1], 0)
                    texture_name = TEXTURE_LIST[int(item[1:])]
                    self.add_voxel(block_pos, self.textures[texture_name])

    def paint_corner(self, position, color_str) -> None:
        self.remove_color(position) # no stacking of paints
        key = vec2key(position)
        paint_pos = self.top_position(position) + Vec3(0, 0, - self.GROUND_OFFSET)
        paint = Paint(paint_pos, color_str)
        paint.tooltip = Tooltip(f'Paint@{vec2tup(position)}: {color_str}')
        self.stacks[key].append(paint)

    def remove_color(self, position) -> None:
        if top := self.top_in_stack(position):
            if top.name == 'paint':
                item = self.stacks[vec2key(position)].pop()
                destroy(item, 1 - self.speed)
        # # Linear logic
        # for item in reversed(self.stacks):
        #     if item.name == 'paint':
        #         destroy(item, 1 - self.speed)

    def corner_color(self, position) -> str:
        '''
        Get the topmost paint object color in the item stack,
        else return None for no paint
        Stack logic: Karel can only access the topmost object/entity
        '''
        if top := self.top_in_stack(position):
            if top.name == 'paint':
                return top.color.name
        return None
        # Linear logic:
        # result = None
        # for item in reversed(self.stacks[vec2key(position)]):
        #     if item.name == 'paint':
        #         return item.color.name
        # return result

    def add_beeper(self, position) -> int:
        key = vec2key(position)
        beeper_pos = self.top_position(position) + Vec3(0, 0, - self.GROUND_OFFSET)
        idx = self.count_beepers(key)
        beeper = Beeper(position = beeper_pos, num_beepers = idx + 1)
        self.stacks[key].append(beeper)
        return idx + 1

    def remove_beeper(self, position) -> int:
        key = vec2key(position)
        beepers_in_stack = self.count_beepers(key)
        if top := self.top_in_stack(position):
            if top.name == 'beeper':
                item = self.stacks[key].pop()
                destroy(item, 1 - self.speed)
                beepers_in_stack -= 1
        return beepers_in_stack

    def add_voxel(self, position, texture) -> None:
        key = vec2key(position)
        block_pos = self.top_position(position) + Vec3(0, 0, - self.GROUND_OFFSET)
        voxel = Voxel(position = block_pos, texture  = texture)
        texture_name = texture.name.split('.')[0]
        position.z = abs(position.z)
        voxel.tooltip = Tooltip(f'Block@{vec2tup(position)}: {texture_name}')
        self.stacks[key].append(voxel)

    def remove_voxel(self, position) -> None:
        if top := self.top_in_stack(position):
            if top.name == 'voxel':
                item = self.stacks[vec2key(position)].pop()
                destroy(item, 1 - self.speed)

    def is_inside(self, position) -> bool:
        return -0.50 < position[0] < self.size.col - 0.5 \
           and -0.50 < position[1] < self.size.row - 0.5

    def top_in_stack(self, position) -> Button:
        item_stack = self.stacks.get(vec2key(position), [])
        if item_stack:
            return item_stack[-1]
        else:
            return None

    def top_position(self, position) -> None:
        if top := self.top_in_stack(position):
            if top.name == 'voxel':
                return top.position + Vec3(0,0, self.GROUND_OFFSET - self.VOXEL_OFFSET_Z)
            if top.name == 'beeper' or top.name == 'paint':
                return top.position + Vec3(0,0, self.GROUND_OFFSET - self.BEEPER_OFFSET_Z)
        return Vec3(position[0], position[1], self.GROUND_OFFSET)

    def wall_exists(self, position, direction) -> bool:
        key = vec2tup(position)[:2]
        for w in self.world_loader.walls:
            if (w.col, w.row, w.direction) == (key[0], key[1], direction):
                return True
        return False

    def get_center(self) -> tuple:
        x_center = self.scale.x // 2 if self.scale.x%2 else self.scale.x // 2 - 0.5
        y_center = self.scale.y // 2 if self.scale.y%2 else self.scale.y // 2 - 0.5
        return (x_center, y_center)

    def get_maxside(self) -> int:
        return max(self.scale.x, self.scale.y)

    def count_beepers(self, key) -> int:
        return self.count_item(key, Beeper)

    def count_blocks(self, key) -> int:
        return self.count_item(key, Voxel)

    def count_item(self, key, object_type) -> int:
        return sum(isinstance(i, object_type) for i in self.stacks.get(key, []))

    def all_beepers(self, key) -> bool:
        return self.same_type(key, Beeper)

    def all_colors(self, key) -> bool:
        return self.same_type(key, Paint)

    def all_same_blocks(self, key) -> tuple:
        is_same_texture = len(set(i.texture for i in self.stacks.get(key, []))) == 1
        return self.same_type(key, Voxel) and is_same_texture

    def same_type(self, key, object_type) -> bool:
        return all(isinstance(i, object_type) for i in self.stacks.get(key, []))

    def stack_string(self, key) -> str:
        '''
        Encodes the stack into a string]
        beeper : 'b'
        voxel  : 'v' + idx of texture
        paint  : 'p' + idx of color
        '''
        stack_list = []
        for item in self.stacks.get(key, []):
            if item.name == 'voxel':
                idx = TEXTURE_LIST.index(item.texture_name)
                stack_list.append(item.name[0] + str(idx))
            elif item.name == 'beeper':
                stack_list.append(item.name[0])
            elif item.name == 'paint':
                idx = COLOR_LIST.index(item.color.name)
                stack_list.append(item.name[0] + str(idx))
        return ' '.join(stack_list)

    @staticmethod
    def get_alt_wall(wall: Wall) -> Wall:
        if wall.direction == Direction.NORTH:
            return Wall(wall.col, wall.row + 1, Direction.SOUTH)
        if wall.direction == Direction.SOUTH:
            return Wall(wall.col, wall.row - 1, Direction.NORTH)
        if wall.direction == Direction.EAST:
            return Wall(wall.col + 1, wall.row, Direction.WEST)
        if wall.direction == Direction.WEST:
            return Wall(wall.col - 1, wall.row, Direction.EAST)
        raise ValueError

    def add_wall(self, wall: Wall) -> None:
        alt_wall = self.get_alt_wall(wall)
        if wall not in self.walls and alt_wall not in self.walls:
            self.walls.add(wall)

    def remove_wall(self, wall: Wall) -> None:
        alt_wall = self.get_alt_wall(wall)
        if wall in self.walls:
            self.walls.remove(wall)
        if alt_wall in self.walls:
            self.walls.remove(alt_wall)
