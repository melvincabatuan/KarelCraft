# from stanfordkarel module
from pathlib import Path
import importlib.util
import traceback as tb
import inspect
import sys

from karelcraft.entities.karel import Karel


class StudentCode:
    """
    This process extracts a module from an arbitary file that contains student code.
    https://stackoverflow.com/questions/67631/how-to-import-a-module-given-the-full-path
    (Credits: stanford.karel module)
    """

    def __init__(self, code_file: Path) -> None:
        if not code_file.is_file():
            raise FileNotFoundError(f"{code_file} could not be found.")

        self.module_name = code_file.stem
        spec = importlib.util.spec_from_file_location(
            self.module_name, code_file.resolve()
        )
        try:
            self.mod = importlib.util.module_from_spec(spec)
            spec.loader.exec_module(self.mod)  # type: ignore
        except SyntaxError as e:
            print(f"Syntax Error: {e}")
            print("\n".join(tb.format_exc(limit=0).split("\n")[1:]))
            sys.exit()

        # Do not proceed if the student has not defined a main function.
        if not hasattr(self.mod, "main"):
            print("Couldn't find the main() function. Are you sure you have one?")
            sys.exit()

    def __repr__(self) -> str:
        return inspect.getsource(self.mod)

    def inject_namespace(self, karel: Karel) -> None:
        """
        This function associates the generic commands the student code to
        specific commands in KarelCraft. (Credits: stanford.karel module)
        """
        functions_to_override = [
            "move",
            "turn_left",
            "pick_beeper",
            "put_beeper",
            "put_block",
            "destroy_block",
            "facing_north",
            "facing_south",
            "facing_east",
            "facing_west",
            "not_facing_north",
            "not_facing_south",
            "not_facing_east",
            "not_facing_west",
            "front_is_clear",
            "beeper_present",
            "beepers_present",
            "no_beeper_present",
            "no_beepers_present",
            "block_present",
            "no_block_present",
            "beepers_in_bag",
            "no_beepers_in_bag",
            "front_is_blocked",
            "left_is_blocked",
            "left_is_clear",
            "right_is_blocked",
            "right_is_clear",
            "paint_corner",
            "remove_paint",
            "corner_color_is",
            "color_present",
            "no_color_present",
        ]
        for func in functions_to_override:
            setattr(self.mod, func, getattr(karel, func))
