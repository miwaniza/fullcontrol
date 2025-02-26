from typing import Optional
from fullcontrol.common import Fan as BaseFan
from fullcontrol.common import Hotend as BaseHotend
from fullcontrol.common import Buildplate as BaseBuildplate
from pydantic import BaseModel

class Fan(BaseModel):
    """Controls fan settings in G-code."""
    speed: Optional[float] = None

    def __init__(self, speed: Optional[float] = None, speed_percent: Optional[float] = None, **kwargs):
        if speed_percent is not None:
            if not 0 <= speed_percent <= 100:
                raise ValueError("Fan speed percentage must be between 0 and 100")
            speed = speed_percent * 255 / 100
        super().__init__(speed=speed, **kwargs)

    def gcode(self, state) -> Optional[str]:
        """Generate G-code for fan control."""
        if self.speed is not None:
            return f"M106 S{int(self.speed)} ; Set fan speed"
        return None


class Hotend(BaseHotend):
    'Extend generic class with gcode method to convert the object to gcode'

    def gcode(self, state) -> Optional[str]:
        'process this instance in a list of steps supplied by the designer to generate and return a line of gcode'
        if self.tool is None:
            if not self.wait:
                return f'M104 S{int(self.temp)} ; set hotend temp and continue'
            return f'M109 S{int(self.temp)} ; set hotend temp and wait'
        if not self.wait:
            return f'M104 S{int(self.temp)} T{self.tool} ; set hotend temp for tool {self.tool} and continue'
        return f'M109 S{int(self.temp)} T{self.tool} ; set hotend temp for tool {self.tool} and wait'


class Buildplate(BaseBuildplate):
    'Extend generic class with gcode method to convert the object to gcode'

    def gcode(self, state) -> Optional[str]:
        'process this instance in a list of steps supplied by the designer to generate and return a line of gcode'
        if not self.wait:
            return f'M140 S{int(self.temp)} ; set bed temp and continue'
        return f'M190 S{int(self.temp)} ; set bed temp and wait'
