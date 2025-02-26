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

    def update_from(self, other):
        """Update this printer's attributes from another printer instance."""
        super().update_from(other)
        if other.print_speed is not None:
            self.print_speed = other.print_speed
            self.speed_changed = True
        if other.travel_speed is not None:
            self.travel_speed = other.travel_speed
            self.speed_changed = True

    def gcode(self, state):
        """Generate G-code for printer settings changes."""
        if self.print_speed is not None:
            state.printer.print_speed = self.print_speed
            state.printer.speed_changed = True
        if self.travel_speed is not None:
            state.printer.travel_speed = self.travel_speed
            state.printer.speed_changed = True
        return ""
