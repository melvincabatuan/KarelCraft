from ursina import *
from pathlib import Path

BLOCK_PATH = 'assets/block'
MODEL_PATH = Path(__file__).absolute().parent.parent / BLOCK_PATH

class Voxel(Button):

    def __init__(self, position=(0, 0, 0), texture=None):
        super().__init__(
            parent=scene,
            position=position + Vec3(0, 0, -0.75),
            rotation=Vec3(0, 90, 90),
            model=MODEL_PATH,
            # model='assets/block',
            origin_y=0.5,
            texture=texture,
            color=color.color(0, 0, random.uniform(0.9, 1)),
            scale=0.5
        )
        self.highlight_color = self.color.tint(.2)
        self.texture_name = self.texture.name.split('_')[0]
