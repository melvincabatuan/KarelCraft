from pathlib import Path
from ursina import *
import random

class TextureLoader:
    def __init__(self) -> None:
        default_texture_path = Path(__file__).absolute().parent.parent.parent / "assets/blocks"
        self.textures = { texture_path.stem.split('_')[0] : load_texture('assets/blocks/'+ texture_path.stem +'.png') \
                        for texture_path in default_texture_path.glob("*.png") }
        self.texture_names = list(self.textures.keys())

    def random_texture(self) -> str:
        return random.choice(self.texture_names)
