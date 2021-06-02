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

INIT_SPEED = 0.75
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


class WorldLoader:
    def __init__(self, world_file: str  = "") -> None:
        """
        Karel World constructor
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


    @staticmethod
    def process_world(world_file: str) -> Path:
        """
        If no world_file is provided, use default world.
        Find world file that matches program name in the current worlds/ directory.
        If not found, search the provided default worlds directory.
        """
        default_worlds_path = Path(__file__).absolute().parent.parent / "worlds"
        if not world_file:
            default_world = default_worlds_path / DEFAULT_WORLD_FILE
            if default_world.is_file():
                print("Using default world...")
                return default_world
            raise FileNotFoundError(
                f"Default world cannot be found in: {default_worlds_path}\n"
                "Please raise an issue on the stanfordkarel GitHub."
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
        available_worlds = "\n".join(
            [f"  {world.stem}" for world in default_worlds_path.glob("*.w")]
        )
        raise FileNotFoundError(
            "The specified file was not one of the provided worlds.\n"
            "Please store custom worlds in a folder named worlds/, "
            f"or use a world listed below:\n{available_worlds}"
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
                # avenue, street
                params["location"] = int(coordinate.group(1)), int(coordinate.group(2))
                continue

            # check to see if the parameter is a direction value
            if param.upper() in (d.name for d in Direction):
                params["direction"] = Direction[param.upper()]

            # check to see if parameter encodes a numerical value or color string
            elif keyword == "color":
                if param.title() not in COLOR_MAP:
                    raise ValueError(
                        f"Error: {param} is invalid parameter for {keyword}."
                    )
                params["color"] = param.title()

            # handle the edge case where Karel has infinite beepers
            elif param in ("infinity", "infinite") and keyword == "beeperbag":
                params["val"] = INFINITY

            # float values are only valid for the speed parameter.
            elif keyword == "speed":
                params["val"] = float(param) if param.isnumeric() else INIT_SPEED

            # must be a digit then
            elif param.isdigit():
                params["val"] = int(param)

            else:
                raise ValueError(f"Error: {param} is invalid parameter for {keyword}.")
        return params

    def load_from_file(self) -> None:
        with open(self.world_file) as f:
            for i, line in enumerate(f):
                # Ignore blank lines and lines with no comma delineator
                line = line.strip()
                if not line:
                    continue

                if KEYWORD_DELIM not in line:
                    print(f"Incorrectly formatted - ignoring line {i} of file: {line}")
                    continue

                keyword, param_str = line.lower().split(KEYWORD_DELIM)

                # only accept valid keywords as defined in world file spec
                # TODO: add error detection for keywords with insufficient parameters
                params = self.parse_parameters(keyword, param_str)

                # handle all different possible keyword cases
                if keyword == "dimension":
                    # set world dimensions based on location values
                    self.columns, self.rows = params["location"]

                elif keyword == "wall":
                    # build a wall at the specified location
                    (avenue, street), direction = (
                        params["location"],
                        params["direction"],
                    )
                    self.walls.add(Wall(avenue, street, direction))

                elif keyword == "beeper":
                    # add the specified number of beepers to the world
                    self.beepers[params["location"]] += params["val"]

                elif keyword == "karel":
                    # Give Karel initial state values
                    self.start_location = params["location"]
                    self.start_direction = params["direction"]

                elif keyword == "beeperbag":
                    # Set Karel's initial beeper bag count
                    self.start_beeper_count = params["val"]

                elif keyword == "speed":
                    # Set delay speed of program execution
                    self.init_speed = params["val"]

                elif keyword == "color":
                    # Set corner color to be specified color
                    self.corner_colors[params["location"]] = params["color"]

                else:
                    print(f"Invalid keyword - ignoring line {i} of world file: {line}")



    @staticmethod
    def get_alt_wall(wall: Wall) -> Wall:
        if wall.direction == Direction.NORTH:
            return Wall(wall.avenue, wall.street + 1, Direction.SOUTH)
        if wall.direction == Direction.SOUTH:
            return Wall(wall.avenue, wall.street - 1, Direction.NORTH)
        if wall.direction == Direction.EAST:
            return Wall(wall.avenue + 1, wall.street, Direction.WEST)
        if wall.direction == Direction.WEST:
            return Wall(wall.avenue - 1, wall.street, Direction.EAST)
        raise ValueError

    def add_wall(self, wall: Wall) -> None:
        alt_wall = self.get_alt_wall(wall)
        if wall not in self.walls and alt_wall not in self.walls:
            self.walls.add(wall)

    # def remove_wall(self, wall: Wall) -> None:
    #     alt_wall = self.get_alt_wall(wall)
    #     if wall in self.walls:
    #         self.walls.remove(wall)
    #     if alt_wall in self.walls:
    #         self.walls.remove(alt_wall)
