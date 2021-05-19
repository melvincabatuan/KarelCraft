from ursina import *

class Beeper(Button):

    def __init__(self, position = (0,0,0), texture = None):
        super().__init__(
            model = 'quad',
            parent = scene,
            scale = 1,
            position = position,
            color = color.green,
            texture = 'icon.png',
            collider = 'box'
        )

