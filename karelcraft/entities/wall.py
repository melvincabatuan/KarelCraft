from ursina import *
from karelcraft.utils.direction import Direction


class Wall(Button):

    def __init__(self, position=(0, 0, -0.5), direction=Direction.EAST):
        super().__init__(
            model='cube',
            parent=scene,
            position=position,
            color=color.white33,
            scale=Vec3(2, 0.05, 1),
        )
        self.position += 0.5*Vec3(direction.value)
        if direction == Direction.EAST or direction == Direction.WEST:
            self.rotation = Vec3(90, 90, 0)
        else:
            self.rotation = Vec3(0, 90, 0)
