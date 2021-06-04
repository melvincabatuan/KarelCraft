# from stanfordkarel module
from pathlib import Path
from typing import Dict, Any, NamedTuple
import collections
import copy
import sys
import re
from karelcraft.utils.direction import Direction
from karelcraft.utils.helpers import  INFINITY

class Wall(NamedTuple):
    col: int
    row: int
    direction: Direction

INIT_SPEED = 0.80
VALID_WORLD_KEYWORDS = [
    "dimension",
    "wall",
    "beeper",
    "karel",
    "speed",
    "beeperbag",
    "color",
]
KEYWORD_DELIM = ":"
PARAM_DELIM = ";"
DEFAULT_WORLD_FILE = "default_world.w"

COLOR_LIST = ["red","black","cyan","white", \
    "smoke", "green", "light_gray", "gray", \
    "dark_gray", "black", "magenta", \
    "orange", "pink",  "blue","yellow", "lime", \
    "turquoise", "azure", "violet", "brown", \
    "olive", "peach", "gold", "salmon"
]


class WorldLoader:
    def __init__(self, world_file: str  = "") -> None:
        """
        WorldLoader constructor
        Parameters:
            world_file: filename containing the initial state of Karel's world
        """

        self.world_file = self.process_world(world_file)

        # Map of beeper locations to the count of beepers at that location
        self.beepers: dict[tuple[int, int], int] = collections.defaultdict(int)

        # Map of corner colors, defaults to ""
        self.corner_colors: dict[tuple[int, int], str] = collections.defaultdict(
            lambda: ""
        )

        # Set of Wall objects placed in the world
        self.walls: set[Wall] = set()

        # Dimensions of the world
        self.rows = 1
        self.columns = 1

        # Initial Karel state saved to enable world reset
        self.start_location = (0, 0)
        self.start_direction = Direction.EAST
        self.start_beeper_count = 0

        # Initial speed slider setting
        self.init_speed = INIT_SPEED

        # If a world file has been specified, load world details from the file
        if self.world_file:
            self.load_from_file()


    def process_world(self, world_file: str) -> Path:
        """
        If no world_file is provided, use default world.
        """
        default_worlds_path = Path(__file__).absolute().parent.parent / "worlds"
        self.available_worlds = [world.stem for world in default_worlds_path.glob("*.w")]
        if not world_file:
            default_world = default_worlds_path / DEFAULT_WORLD_FILE
            if default_world.is_file():
                print("Using default world...")
                return default_world
            raise FileNotFoundError(
                f"Default world cannot be found in: {default_worlds_path}\n"
            )

        world_filepath = Path(world_file)
        if world_filepath.is_file():
            return world_filepath

        worlds_folder = Path("worlds")
        for worlds_path in (worlds_folder, default_worlds_path):
            if worlds_path.is_dir():
                full_world_path = worlds_path / f"{world_file}.w"
                if full_world_path.is_file():
                    return full_world_path

        if not worlds_folder.is_dir():
            print("Could not find worlds/ folder in current directory.\n")

        sys.tracebacklimit = 0
        available_worlds_str = "\n".join(self.available_worlds)
        raise FileNotFoundError(
            "The specified file was not one of the provided worlds.\n"
            "Please store custom worlds in a folder named worlds/, "
            f"or use a world listed below:\n{available_worlds_str}"
            "\nPass the default world as a parameter in run_karel_program().\n"
            "    e.g. run_karel_program('checkerboard_karel')"
        )



    @staticmethod
    def parse_parameters(keyword: str, param_str: str) -> Dict[str, Any]:
        params: dict[str, Any] = {}
        for param in param_str.split(PARAM_DELIM):
            param = param.strip()

            # check to see if parameter encodes a location
            coordinate = re.match(r"\((\d+),\s*(\d+)\)", param)
            if coordinate:
                # col, row
                params["location"] = int(coordinate.group(1)), int(coordinate.group(2))
                continue

            if param.upper() in (d.name for d in Direction):
                params["direction"] = Direction[param.upper()]

            elif keyword == "color":
                if param not in COLOR_LIST:
                    raise ValueError(
                        f"Error: {param} is invalid parameter for {keyword}."
                )
                params["color"] = param

            elif param in ("infinity", "infinite") and keyword == "beeperbag":
                params["val"] = INFINITY

            elif keyword == "speed":
                try:
                    params["val"] = float(param)
                except ValueError as e:
                    params["val"] = INIT_SPEED
                    print(f"Error: {param} is an invalid parameter for {keyword}. Using default.")
            elif param.isdigit():
                params["val"] = int(param)

            else:
                raise ValueError(f"Error: {param} is invalid parameter for {keyword}.")
        return params

    def load_from_file(self) -> None:
        with open(self.world_file) as f:
            for i, line in enumerate(f):
                line = line.strip()
                if not line:
                    continue

                if KEYWORD_DELIM not in line:
                    print(f"Incorrectly formatted - ignoring line {i} of file: {line}")
                    continue

                keyword, param_str = line.lower().split(KEYWORD_DELIM)
                params = self.parse_parameters(keyword, param_str)

                if keyword == "dimension":
                    self.columns, self.rows = params["location"]

                elif keyword == "wall":
                    (col, row), direction = (
                        params["location"],
                        params["direction"],
                    )
                    self.walls.add(Wall(col, row, direction))

                elif keyword == "beeper":
                    self.beepers[params["location"]] += params["val"]

                elif keyword == "karel":
                    self.start_location = params["location"]
                    self.start_direction = params["direction"]

                elif keyword == "beeperbag":
                    self.start_beeper_count = params["val"]

                elif keyword == "speed":
                    self.init_speed = params["val"]

                elif keyword == "color":
                    self.corner_colors[params["location"]] = params["color"]

                else:
                    print(f"Invalid keyword - ignoring line {i} of world file: {line}")



    # @staticmethod
    # def get_alt_wall(wall: Wall) -> Wall:
    #     if wall.direction == Direction.NORTH:
    #         return Wall(wall.avenue, wall.street + 1, Direction.SOUTH)
    #     if wall.direction == Direction.SOUTH:
    #         return Wall(wall.avenue, wall.street - 1, Direction.NORTH)
    #     if wall.direction == Direction.EAST:
    #         return Wall(wall.avenue + 1, wall.street, Direction.WEST)
    #     if wall.direction == Direction.WEST:
    #         return Wall(wall.avenue - 1, wall.street, Direction.EAST)
    #     raise ValueError

    # def add_wall(self, wall: Wall) -> None:
    #     alt_wall = self.get_alt_wall(wall)
    #     if wall not in self.walls and alt_wall not in self.walls:
    #         self.walls.add(wall)

    # def remove_wall(self, wall: Wall) -> None:
    #     alt_wall = self.get_alt_wall(wall)
    #     if wall in self.walls:
    #         self.walls.remove(wall)
    #     if alt_wall in self.walls:
    #         self.walls.remove(alt_wall)
