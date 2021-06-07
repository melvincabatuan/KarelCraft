from ursina import *


class Paint(Button):

    def __init__(self, position=(0, 0, 0), name='green'):
        super().__init__(
            model='quad',
            parent=scene,
            scale=1,
            position=position,
            color=color.colors[name],
            collider='box',
        )
