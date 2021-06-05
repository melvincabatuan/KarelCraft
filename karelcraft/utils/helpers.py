# Helpers and constants

INFINITY  = -1


'''
Converts Vec2 or Vec3 to int tuple
'''
vec2tup = lambda v: tuple(map(int, v))


'''
Converts Vec2 or Vec3 to int tuple key or 2D position
'''
vec2key = lambda v: tuple(map(int, v))[:2]


class KarelException(Exception):
    def __init__(self, position: tuple,
        direction: str,
        action: str,
        message: str) -> None:
        super().__init__()
        self.position  = position
        self.direction = direction
        self.action    = action
        self.message   = message

    def __str__(self) -> str:
        return (
            f"Karel crashed while on position {self.position}, "
            f"facing {self.direction}\nInvalid action: {self.message}"
        )
