from typing import Optional

class ManualGcode:
    """Class for handling manual G-code commands."""
    def __init__(self, gcode: str = None):
        if gcode is not None and not isinstance(gcode, str):
            raise ValueError("G-code must be a string")
        self.gcode = gcode.strip() if gcode else ""

    def gcode(self, state) -> Optional[str]:
        """Return the manual G-code command."""
        return self.gcode if self.gcode else None