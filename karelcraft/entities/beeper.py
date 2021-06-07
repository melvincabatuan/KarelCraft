from ursina import *


class Beeper(Entity):

    def __init__(self, position=(0, 0, 0), num_beepers=0):
        super().__init__(
            model='quad',
            parent=scene,
            scale=1.1,
            position=position,
            color=color.green,
            texture='icon.png',
            collider='box'
        )
        self.num_beepers = num_beepers
        self.create_text()

    def create_text(self):
        msg = f'{self.num_beepers}'
        self.txt = Text(
            text=msg,
            parent=self,
            scale=12,
            position=self.origin,
            color=color.red,
        )
        self.txt.z -= 0.01
        self.txt.y -= 0.30
        self.txt.x -= 0.14
        # self.txt.create_background(radius=1, padding=1)
