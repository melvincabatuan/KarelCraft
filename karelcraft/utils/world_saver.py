'''
This class saves the world state

'''

from karelcraft.entities.karel import Karel


class WorldSaver:
    def __init__(self, karel: Karel) -> None:
        self.karel = karel
        self.world = karel.world
