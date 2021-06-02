from ursina import *
from collections import defaultdict
from karelcraft.entities.voxel import Voxel
from karelcraft.entities.beeper import Beeper
from karelcraft.entities.paint import Paint
from karelcraft.entities.wall import Wall
from karelcraft.utils.helpers import vec2tup
from karelcraft.utils.world_loader import WorldLoader

class World(Entity):

    GROUND_POSITION = (0,0,-0.5)

    def __init__(self, world_file: str) -> None:
        super().__init__(
            model    = 'quad',
            parent   = scene,
            color    = rgb(125, 125, 125),
        )
        self.loader = WorldLoader(world_file)
        self.set_position((self.loader.columns / 2, self.loader.rows / 2, 0))
        self.scale = Vec3(self.loader.columns, self.loader.rows, 0)
        self.create_grid()
        self.position_correction()
        self.beeper_offset_z = 0.1
        self.voxel_offset_z  = 1
        self.beeper_position_z = self.beeper_offset_z
        self.speed =  self.loader.init_speed

        self.paints  : dict[tuple[int, int], Paint]  = defaultdict(None)
        self.voxels  : dict[tuple[int, int], list]   = defaultdict(list)
        self.beepers : dict[tuple[int, int], list]   = defaultdict(list)
        self.load_beepers()
        self.load_walls()

    def position_correction(self):
        '''
        Offset used for centering the position to intersection,
        e.g. (0,0),(1,1), not (0.5, 0.5)
        '''
        self.world_position -= Vec3((0.5, 0.5, -0.01))

    def create_grid(self, height = -0.001):
        Entity(model = Grid(self.loader.columns, self.loader.rows, thickness=1.5),
            scale = 1,
            position = (self.origin.x, self.origin.y, height),
            color = color.white,
            parent = self
        )

    def load_beepers(self) -> None:
        for key, val in self.loader.beepers.items():
            for _ in range(val):
                self.add_beeper(key)

    def load_walls(self) -> None:
        for w in self.loader.walls:
            wall_pos = Vec3(w.col, w.row, -1)
            wall_object = Wall(position = wall_pos, direction = w.direction)

    def paint_corner(self, position, key) -> None:
        paint = Paint(position, key)
        paint.tooltip = Tooltip(f'Paint@{vec2tup(position)}: {key}')
        self.paints[vec2tup(position)] = paint

    def corner_color(self, position) -> str:
        return self.paints.get(tuple(position))

    def add_beeper(self, key) -> int:
        idx_in_stack = len(self.beepers.get(key,[]))
        beeper_pos = Vec3(key[0], key[1],-idx_in_stack*self.beeper_offset_z)
        beeper = Beeper(position = beeper_pos, num_beepers = idx_in_stack + 1)
        self.beepers[key].append(beeper)
        return idx_in_stack + 1

    def remove_beeper(self, position) -> int:
        key = vec2tup(position)[:2]
        element = self.beepers[key].pop()
        destroy(element, 1 - self.speed)
        return len(self.beepers.get(key,[]))

    def add_voxel(self, position, texture) -> None:
        voxel = Voxel(position = position, texture  = texture)
        texture_name = texture.name.split('.')[0]
        position.z = abs(position.z)
        voxel.tooltip = Tooltip(f'Block@{vec2tup(position)}: {texture_name}')
        self.voxels[vec2tup(position)[:2]].append(voxel)

    def remove_voxel(self, position) -> int:
        key = vec2tup(position)[:2]
        element = self.voxels[key].pop()
        destroy(element, 1 - self.speed)
        return len(self.voxels.get(key,[]))

    def remove_color(self, position) -> None:
        element = self.paints.pop(position, None)
        destroy(element, 1 - self.speed)

    def is_inside(self, position) -> bool:
        return -0.50 < position[0] < self.loader.columns - 0.5 \
           and -0.50 < position[1] < self.loader.rows - 0.5

    def top_position(self, position) -> None:
        key = vec2tup(position)[:2]
        top = Vec3(position.x, position.y, self.GROUND_POSITION[-1])
        if self.beepers.get(key,[]):
            beeper_top = self.beepers.get(key,[])[-1].position + Vec3(self.GROUND_POSITION)
            if beeper_top.z < top.z:
                top = beeper_top
        if self.voxels.get(key,[]):
            block_top = self.voxels.get(key,[])[-1].position + Vec3(self.GROUND_POSITION)
            if block_top.z < top.z:
                top = block_top + Vec3(0,0,-0.2)
        return top

    def clear_objects(self) -> None:
        for k in self.paints.keys():
            destroy(self.paints[k])
        beepers_to_destroy = [b for k in self.beepers for b in self.beepers[k]]
        for beeper in beepers_to_destroy:
            destroy(beeper)
        blocks_to_destroy  = [b for k in self.voxels for b in self.voxels[k]]
        for block in blocks_to_destroy:
            destroy(block)


    def wall_exists(self, position, direction) -> bool:
        key = vec2tup(position)[:2]
        for w in self.loader.walls:
            if (w.col, w.row, w.direction) == (key[0], key[1], direction):
                return True
        return False
