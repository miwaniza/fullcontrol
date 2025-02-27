from typing import Optional
from pydantic import Field
from fullcontrol.common import BaseModelPlus


class Fan(BaseModelPlus):
    """
    Represents a fan with a speed percentage.

    This class manages fan settings in a 3D printing context, allowing control
    over fan speed as a percentage.

    Attributes:
        speed_percent (Optional[int]): The speed of the fan as a percentage (0-100).
            Value is validated to be between 0 and 100 inclusive.
    """
    speed_percent: Optional[int] = Field(None, ge=0, le=100)


class Hotend(BaseModelPlus):
    """
    Represents a hotend component of a 3D printer.

    This class manages hotend temperature settings and provides control over
    whether the printing process should wait for the temperature to be reached
    before continuing.

    Attributes:
        temp (Optional[int]): The temperature of the hotend in degrees Celsius.
        wait (Optional[bool]): If True, the system will wait for the temperature
            to be reached before continuing. Defaults to False.
        tool (Optional[int]): The tool number for multi-tool printers. Used to 
            specify which hotend to control in a multi-extruder setup.
    """
    temp: Optional[int] = None
    wait: Optional[bool] = False
    tool: Optional[int] = None


class Buildplate(BaseModelPlus):
    """
    Represents a buildplate (print bed) of a 3D printer.

    This class manages the buildplate temperature settings and provides control
    over whether the printing process should wait for the temperature to be reached
    before continuing.

    Attributes:
        temp (Optional[int]): The temperature of the buildplate in degrees Celsius.
        wait (Optional[bool]): If True, the system will wait for the temperature
            to be reached before continuing. Defaults to False.
    """
    temp: Optional[int] = None
    wait: Optional[bool] = False
