from enum import Enum, unique


@unique
class Direction(Enum):
    EAST     = (1, 0, 0)
    SOUTH    = (0, -1, 0)
    WEST     = (-1, 0, 0)
    NORTH    = (0, 1, 0)

    def __lt__(self, other: object) -> bool:
        if isinstance(other, Direction):
            return self.value < other.value
        return NotImplemented

    def __repr__(self) -> str:
        return str(self.value)

    @staticmethod
    def rotate90(direction, mode = 'clockwise'):
        NEXT_NWSE = {
            Direction.NORTH: Direction.WEST,
            Direction.WEST:  Direction.SOUTH,
            Direction.SOUTH: Direction.EAST,
            Direction.EAST:  Direction.NORTH,
        }
        if mode == 'clockwise':
            return NEXT_NWSE[direction]
        else:
            NEXT_NWSE_CCW = {
                v: k for k, v in NEXT_NWSE.items()
            }
            return NEXT_NWSE_CCW[direction]

    @staticmethod
    def opposite(direction):
        opposite_dir = {
            Direction.NORTH: Direction.SOUTH,
            Direction.WEST:  Direction.EAST,
            Direction.SOUTH: Direction.NORTH,
            Direction.EAST:  Direction.WEST,
        }
        return opposite_dir[direction]

    @staticmethod
    def angle(direction):
        angle = {
            Direction.NORTH: 360,
            Direction.WEST:  270,
            Direction.SOUTH: 180,
            Direction.EAST:  90,
        }
        return angle[direction]
