from typing import Optional
from fullcontrol.common import BaseModelPlus


class Printer(BaseModelPlus):
    """
    A class representing a 3D printer.

    Attributes:
        print_speed (Optional[int]): The speed at which the printer prints, in units per minute.
        travel_speed (Optional[int]): The speed at which the printer moves between printing locations, in units per minute.
        speed_changed (Optional[bool]): Flag to track if speed settings have changed.
    """
    print_speed: Optional[float] = None
    travel_speed: Optional[float] = None
    speed_changed: Optional[bool] = False

    def gcode(self, state):
        """Generate G-code for printer settings changes."""
        state.printer.update_from(self)
        if self.print_speed is not None:
            state.printer.speed_changed = True
            return f"G1 F{self.print_speed}"
        return ""
