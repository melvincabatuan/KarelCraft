from ursina import *
import collections
from karelcraft.constants import MAP_SIZE, WAIT_TIME
from karelcraft.entities.voxel import Voxel
from karelcraft.entities.beeper import Beeper
from karelcraft.entities.color_paint import ColorPaint


class World(Entity):
    POSITION_OFFSET = Vec3(0.5, 0.5, 0.01)
    def __init__(self, MAP_SIZE: MAP_SIZE) -> None:
        super().__init__(
        position =  (MAP_SIZE / 2, MAP_SIZE / 2, 0),
        model    = 'quad',
        scale    = MAP_SIZE,
        parent   = scene,
        color    = rgb(102, 102, 102)
        )
        self.beepers: dict[tuple[int, int], Beeper]     = collections.defaultdict(None)
        self.voxels : dict[tuple[int, int], Voxel]      = collections.defaultdict(None)
        self.paints : dict[tuple[int, int], ColorPaint] = collections.defaultdict(None)
        self.grid_scale = 1
        self.create_grid()
        self.position_correction()
        # centering the position to intersection, e.g. (0,0),(1,1), not (0.5, 0.5)

    def position_correction(self):
        self.world_position -= self.POSITION_OFFSET

    def create_grid(self, height = -0.001):
        Entity(model = Grid(MAP_SIZE, MAP_SIZE, thickness=1.2),
            scale = self.grid_scale,
            position = (self.origin.x, self.origin.y, height),
            color = color.white,
            parent = self
        )

    def paint_corner(self, position, key) -> None:
        paint = ColorPaint(position, key)
        paint.tooltip = Tooltip(f'{position}: {key}')
        self.paints[tuple(position)] = paint

    def corner_color(self, position) -> str:
        return self.paints.get((position.x, position.y))

    def add_beeper(self, position) -> None:
        beeper = Beeper(position = position)
        beeper.tooltip = Tooltip(f'{position}')
        self.beepers[tuple(position)] = beeper

    def remove_beeper(self, position) -> None:
        element = self.beepers.pop(position, None)
        destroy(element, WAIT_TIME)

    def add_voxel(self, position, texture) -> None:
        voxel = Voxel(position = position, texture  = texture)
        voxel.tooltip = Tooltip(f'{position}')
        self.voxels[tuple(position)] = voxel
        print(self.voxels)

    def remove_voxel(self, position) -> None:
        element = self.voxels.pop(position, None)
        destroy(element, WAIT_TIME)
        del element

    def remove_color(self, position) -> None:
        element = self.paints.pop(position, None)
        destroy(element, WAIT_TIME)

    def is_inside(self, position) -> bool:
        return -0.50 < position[0] < MAP_SIZE - 0.5 \
           and -0.50 < position[1] < MAP_SIZE - 0.5

    def destroy_voxels():
        pass
