from ursina import *

class Paint(Button):

    def __init__(self, position = (0,0,0), key = 'green'):
        super().__init__(
            model = 'quad',
            parent = scene,
            scale = 1,
            position = position,
            color = color.colors[key],
            collider = 'box',
        )

