from typing import Optional, Any
from fullcontrol.common import BaseModelPlus
from math import pi


class ExtrusionGeometry(BaseModelPlus):
    """
    Geometric description of the printed extrudate.
    
    This class defines the cross-sectional geometry of extruded material in 3D printing,
    allowing calculation of the extrusion area based on different geometric models.
    
    Attributes:
        area_model (Optional[str]): Specifies how the cross-sectional area is defined.
            Options include:
            - 'rectangle': Rectangular cross-section (requires width and height)
            - 'stadium': Stadium shape cross-section (requires width and height)
            - 'circle': Circular cross-section (requires diameter)
            - 'manual': User-specified area value
        width (Optional[float]): Width of printed line for 'rectangle' or 'stadium' models.
        height (Optional[float]): Height of printed line for 'rectangle' or 'stadium' models.
        diameter (Optional[float]): Diameter of printed line for 'circle' model.
        area (Optional[float]): Cross-sectional area of the extrudate. Automatically 
            calculated based on the area_model and relevant attributes, or set manually 
            when area_model is 'manual'.
    """
    # area_model options: 'rectangle' / 'stadium' / 'circle' / 'manual':
    area_model: Optional[str] = None
    # width of printed line for area_model = rectangle or stadium:
    width: Optional[float] = None
    # height of printed line for area_model = rectangle or stadium:
    height: Optional[float] = None
    # diameter of printed line for area_model = circle:
    diameter: Optional[float] = None
    # automatically calculated based on area_model and relevant attributes
    area: Optional[float] = None

    def update_area(self) -> float:
        """
        Update the area attribute based on the area_model and relevant attributes.
        
        This method calculates the cross-sectional area of the extruded material
        based on the specified area_model and the relevant geometric parameters.
        For the 'manual' area_model, the area attribute must be set externally.
        
        Returns:
            float: The calculated area (also stored in the area attribute)
        """
        if self.area_model == "rectangle":
            self.area = self.width * self.height
        elif self.area_model == "stadium":
            self.area = ((self.width - self.height) * self.height) + (pi * (self.height / 2) ** 2)
        elif self.area_model == "circle":
            self.area = (pi * (self.diameter / 2) ** 2)
        elif self.area_model == "manual":
            pass


class StationaryExtrusion(BaseModelPlus):
    """
    Represents stationary extrusion in a 3D printer.

    This class is used to control the extrusion of a specific volume of material
    at a set speed while the printer's nozzle remains stationary. This is useful
    for operations like priming the nozzle or creating specific features.
    Negative volumes indicate retraction of material.

    Attributes:
        volume (float): The volume of material to extrude in cubic millimeters.
            Negative values indicate retraction.
        speed (int): The speed at which to extrude the material, typically in mm/min.
            The actual units depend on the G-code format used by the printer.
    """

    # design attributes to control one-off extrusion without nozzle movement:
    volume: float
    speed: int


class Extruder(BaseModelPlus):
    """
    Represents an extruder for controlling material extrusion.

    This class provides control over the extrusion state (on/off) and 
    retraction settings during a 3D printing process. It allows specification
    of whether extrusion should be active and the retraction distance when
    turning extrusion off.

    Attributes:
        on (Optional[bool]): Indicates whether extrusion is active (True) or
            inactive (False). When None, the extrusion state is unchanged.
        retraction (Optional[float]): The retraction distance in millimeters
            when turning extrusion off. Only applied when turning extrusion off.
        relative_gcode (Optional[bool]): Whether to use relative extrusion
            in G-code (E values are relative to the current position).
    """
    on: Optional[bool] = None
    retraction: Optional[float] = None
    relative_gcode: Optional[bool] = None
