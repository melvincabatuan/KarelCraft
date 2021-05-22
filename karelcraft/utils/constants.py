TITLE = "KarelCraft"

# Map
MAP_SIZE = 18
WORLD_OFFSET = (0.5, 0.5, -0.01) # corrects world_position

# Karel
WAIT_TIME = 0.2
INFINITY  = -1
INIT_BEEPERS = INFINITY

# Misc
EAST     = (1, 0, 0)
SOUTH    = (0, -1, 0)
WEST     = (-1, 0, 0)
NORTH    = (0, 1, 0)

NWSE_MAP = {
    EAST:  'EAST',
    WEST:  'WEST',
    NORTH: 'NORTH',
    SOUTH: 'SOUTH'
}

NEXT_NWSE = {
        NORTH: WEST,
        WEST:  SOUTH,
        SOUTH: EAST,
        EAST:  NORTH,
}

NEXT_NWSE_CCW = {
        v: k for k, v in NEXT_NWSE.items()
}
