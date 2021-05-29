from ursina import *
from collections import defaultdict
from karelcraft.entities.voxel import Voxel
from karelcraft.entities.beeper import Beeper
from karelcraft.entities.paint import Paint
from karelcraft.utils.constants import MAP_SIZE, WAIT_TIME, WORLD_OFFSET
from karelcraft.utils.helpers import vec2tup


class World(Entity):
    GROUND_POSITION = (0,0,-0.5)
    def __init__(self, MAP_SIZE: MAP_SIZE) -> None:
        super().__init__(
        position =  (MAP_SIZE / 2, MAP_SIZE / 2, 0),
        model    = 'quad',
        scale    = MAP_SIZE,
        parent   = scene,
        color    = rgb(102, 102, 102)
        )
        self.grid_scale = 1
        self.create_grid()
        self.position_correction()
        self.beeper_offset_z = 0.1 # 1/MAP_SIZE
        self.voxel_offset_z  = 1 # 1/MAP_SIZE
        self.beeper_position_z = self.beeper_offset_z
        self.paints  : dict[tuple[int, int], Paint]  = defaultdict(None)
        self.voxels  : dict[tuple[int, int], list]   = defaultdict(list)
        self.beepers : dict[tuple[int, int], list]   = defaultdict(list)

    def position_correction(self):
        '''
        Offset used for centering the position to intersection,
        e.g. (0,0),(1,1), not (0.5, 0.5)
        '''
        self.world_position -= Vec3(WORLD_OFFSET)

    def create_grid(self, height = -0.001):
        Entity(model = Grid(MAP_SIZE, MAP_SIZE, thickness=1.2),
            scale = self.grid_scale,
            position = (self.origin.x, self.origin.y, height),
            color = color.white,
            parent = self
        )

    def paint_corner(self, position, key) -> None:
        paint = Paint(position, key)
        paint.tooltip = Tooltip(f'Paint@{vec2tup(position)}: {key}')
        self.paints[vec2tup(position)] = paint

    def corner_color(self, position) -> str:
        print(tuple(position))
        return self.paints.get(tuple(position))

    def add_beeper(self, position, num_in_stack) -> None:
        beeper = Beeper(position = position, num_beepers = num_in_stack)
        self.beepers[vec2tup(position)[:2]].append(beeper)

    def remove_beeper(self, position) -> int:
        key = vec2tup(position)[:2]
        element = self.beepers[key].pop()
        destroy(element, WAIT_TIME)
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
        destroy(element, WAIT_TIME)
        return len(self.voxels.get(key,[]))

    def remove_color(self, position) -> None:
        element = self.paints.pop(position, None)
        destroy(element, WAIT_TIME)

    def is_inside(self, position) -> bool:
        return -0.50 < position[0] < MAP_SIZE - 0.5 \
           and -0.50 < position[1] < MAP_SIZE - 0.5

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


