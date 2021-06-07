from ursina import *


class Voxel(Button):

    def __init__(self, position=(0, 0, 0), texture=None):
        super().__init__(
            parent=scene,
            position=position + Vec3(0, 0, -0.75),
            rotation=Vec3(0, 90, 90),
            model='assets/block',
            origin_y=0.5,
            texture=texture,
            color=color.color(0, 0, random.uniform(0.9, 1)),
            scale=0.5
        )
        self.highlight_color = self.color.tint(.2)
        self.texture_name = self.texture.name.split('_')[0]
