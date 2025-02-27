from typing import Optional
from fullcontrol.common import BaseModelPlus


class Point(BaseModelPlus):
    """
    Represents a point in 3D space with x, y, and z cartesian components.
    
    The Point class is a fundamental building block in FullControl designs, 
    representing positions in 3D space for toolpaths and other geometric operations.
    
    Attributes:
        x (Optional[float]): The x-coordinate in Cartesian space. Default is None.
        y (Optional[float]): The y-coordinate in Cartesian space. Default is None.
        z (Optional[float]): The z-coordinate in Cartesian space. Default is None.
    
    Example:
        >>> import fullcontrol as fc
        >>> point = fc.Point(x=10, y=20, z=30)
    """
    x: Optional[float] = None
    y: Optional[float] = None
    z: Optional[float] = None
