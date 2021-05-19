from ursina import *
import collections
from karelcraft.constants import MAP_SIZE
from karelcraft.entities.voxel import Voxel
from karelcraft.entities.beeper import Beeper
from karelcraft.entities.color_paint import ColorPaint

class World:
    position_offset = Vec3(0.5, 0.5, 0.01)
    def __init__(self, MAP_SIZE: MAP_SIZE) -> None:
        self.beepers: dict[tuple[int, int], int] = collections.defaultdict(int)
        self.voxels : dict[tuple[int, int], int] = collections.defaultdict(int)
        self.paints : dict[tuple[int, int], str] = collections.defaultdict(lambda: "")
        # Credits: StanislavPetrovV ( https://github.com/StanislavPetrovV/Snake3D )
        # for the headstart on these entities.
        Entity(model='quad',
            scale=MAP_SIZE,
            position=(MAP_SIZE / 2, MAP_SIZE / 2, 0),
            color=rgb(102, 102, 102)
            )
        Entity(model=Grid(MAP_SIZE, MAP_SIZE),
            scale=MAP_SIZE,
            position=(MAP_SIZE / 2, MAP_SIZE / 2, -0.01),
            color=color.white)

    def paint_corner(self, position, key) -> None:
        paint = ColorPaint(position, key)
        paint.tooltip = Tooltip(f'{self.grid_position(position)}: {key}')
        self.paints[(position.x, position.y)] = key

    def corner_color(self, position) -> str:
        return self.paints.get((position.x, position.y))

    def add_beeper(self, position) -> None:
        beeper = Beeper(position = position)
        beeper.tooltip = Tooltip(f'{self.grid_position(position)}')
        self.beepers[(position.x, position.y)] += 1

    def remove_beeper(self, position) -> None:
        self.beepers[(position.x, position.y)] -= 1

    def add_voxel(self, position, texture) -> None:
        voxel = Voxel(position = position, texture  = texture)
        voxel.tooltip = Tooltip(f'{self.grid_position(position)}')
        self.voxels[(position.x, position.y)] += 1

    def remove_voxel(self, position) -> None:
        self.voxels[(position.x, position.y)] -= 1

    def grid_position(self, position) -> tuple:
        current_position = position + self.position_offset
        return tuple(map(int, current_position))

    def is_inside(self, position) -> bool:
        return 0 < position[0] < MAP_SIZE and 0 <  position[1] < MAP_SIZE
