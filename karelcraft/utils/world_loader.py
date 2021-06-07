# from stanfordkarel module
from pathlib import Path
from typing import Dict, Any, NamedTuple
import collections
import copy
import sys
import re
from karelcraft.utils.direction import Direction
from karelcraft.utils.helpers import INFINITY
from collections import defaultdict


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
    "block",
    "stack",
]
KEYWORD_DELIM = ":"
PARAM_DELIM = ";"
DEFAULT_WORLD_FILE = "default_world.w"

COLOR_LIST = ["red", "black", "cyan", "white",
              "smoke", "green", "light_gray", "gray",
              "dark_gray", "black", "magenta",
              "orange", "pink",  "blue", "yellow", "lime",
              "turquoise", "azure", "violet", "brown",
              "olive", "peach", "gold", "salmon"
              ]
TEXTURE_LIST = ['brick', 'diamond', 'dirt', 'dlsu',
                'emerald', 'gold', 'grass', 'lava', 'leaves',
                'obsidian', 'rose', 'sand', 'snow', 'sponge',
                'stonebrick', 'stone', 'wood']


class WorldLoader:
    def __init__(self, world_file: str = "") -> None:
        """
        WorldLoader constructor
        Parameters:
            world_file: filename containing the initial state of Karel's world
        """
        self.world_file = self.process_world(world_file.split('.')[0])
        self.beepers: dict[tuple[int, int], int] = collections.defaultdict(int)
        self.corner_colors: dict[tuple[int, int], str] = collections.defaultdict(lambda: "")
        self.blocks: dict[tuple[int, int], tuple[str, int]] = collections.defaultdict(lambda: ('', 0))
        self.stack_strings: dict[tuple[int, int], str] = collections.defaultdict(lambda: "")

        self.walls: set[Wall] = set()
        # Initial dimensions of the world
        self.rows = 1
        self.columns = 1
        # Initial Karel state
        self.start_location = (0, 0)
        self.start_direction = Direction.EAST
        self.start_beeper_count = 0
        # Initial speed slider setting
        self.init_speed = INIT_SPEED
        # If a world file has been specified, load world details from the file
        if self.world_file:
            self.load_from_file()

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

                elif keyword == "block":
                    self.blocks[params["location"]] = (
                        params["texture"], params["val"])

                elif keyword == "stack":
                    self.stack_strings[params["location"]
                                       ] = params["stack_string"]

                else:
                    print(f"Invalid keyword - ignoring line {i} of world file: {line}")

    @staticmethod
    def parse_parameters(keyword: str, param_str: str) -> Dict[str, Any]:
        params: dict[str, Any] = {}
        for param in param_str.split(PARAM_DELIM):
            param = param.strip()

            # check to see if parameter encodes a location
            coordinate = re.match(r"\((\d+),\s*(\d+)\)", param)
            if coordinate:
                # col, row
                params["location"] = int(
                    coordinate.group(1)), int(coordinate.group(2))
                continue

            if param.upper() in (d.name for d in Direction):
                params["direction"] = Direction[param.upper()]

            elif keyword == "color":
                if param not in COLOR_LIST:
                    raise ValueError(
                        f"Error: {param} is invalid parameter for {keyword}."
                    )
                params["color"] = param

            elif keyword == "block" and not param.isdigit():
                if param not in TEXTURE_LIST:
                    raise ValueError(
                        f"Error: {param} is invalid parameter for {keyword}."
                    )
                params["texture"] = param

            elif keyword == "stack":
                if all(c[0] in ['b', 'p', 'v'] for c in param.split()):  # TODO: can be improved
                    params["stack_string"] = param
                else:
                    raise ValueError(
                        f"Error: {param} is invalid parameter for {keyword}."
                    )

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

    def process_world(self, world_file: str) -> Path:
        """
        If no world_file is provided, use default world.
        """
        default_worlds_path = Path(
            __file__).absolute().parent.parent / "worlds"
        self.available_worlds = [
            world.stem for world in default_worlds_path.glob("*.w")]
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
