from fullcontrol.common import linspace
from fullcontrol.geometry import Point, polar_to_point, ramp_xyz, ramp_polar
from math import tau, sin, cos

def _clean_float(x: float, epsilon: float = 1e-10) -> float:
    """
    Clean up floating point values that are very close to zero.
    
    This helper function prevents floating point precision issues by
    setting values that are extremely close to zero to exactly zero.
    
    Args:
        x (float): The floating point value to clean
        epsilon (float, optional): The threshold below which values are 
            considered zero. Defaults to 1e-10.
    
    Returns:
        float: Either 0.0 if |x| < epsilon, or the original value x
    """
    return 0.0 if abs(x) < epsilon else x

def arcXY(centre: Point, radius: float, start_angle: float, arc_angle: float, segments: int = 100) -> list:
    """
    Generate a 2D circular arc in the XY plane.
    
    This function creates a list of points forming a circular arc in the XY plane.
    The Z coordinate of each point will be the same as the Z coordinate of the center point.
    Angles are defined in radians.
    
    Args:
        centre (Point): The center point of the arc
        radius (float): The radius of the arc
        start_angle (float): The starting angle in radians
        arc_angle (float): The angular extent of the arc in radians
        segments (int, optional): The number of segments to divide the arc into. 
            More segments result in a smoother arc. Defaults to 100.
    
    Returns:
        list: A list of Points representing the arc
    
    Example:
        >>> import fullcontrol as fc
        >>> from math import pi
        >>> center = fc.Point(x=50, y=50, z=0)
        >>> half_circle = arcXY(center, 10, 0, pi, 20)  # 20-segment half circle
    """
    a_steps = linspace(start_angle, start_angle+arc_angle, segments+1)
    points = [polar_to_point(centre, radius, a) for a in a_steps]
    # Clean up floating point errors
    for p in points:
        p.x = _clean_float(p.x)
        p.y = _clean_float(p.y)
    return points


def variable_arcXY(centre: Point, start_radius: float, start_angle: float, arc_angle: float, segments: int = 100, radius_change: float = 0, z_change: float = 0) -> list:
    """
    Generate an arc with optionally varying radius and Z-position.
    
    This function creates an arc that can simultaneously vary in radius and height,
    making it useful for spiral ramps and other complex shapes. The arc begins at
    the specified start_radius and the Z-position of the center point, and can
    change over its length according to the radius_change and z_change parameters.
    
    Args:
        centre (Point): The center point of the arc
        start_radius (float): The starting radius of the arc
        start_angle (float): The starting polar angle in radians
        arc_angle (float): The angular extent of the arc in radians
        segments (int, optional): The number of segments to divide the arc into.
            More segments result in a smoother arc. Defaults to 100.
        radius_change (float, optional): The total change in radius over the arc.
            Positive values increase the radius, negative values decrease it.
            Defaults to 0 (constant radius).
        z_change (float, optional): The total change in Z position over the arc.
            Positive values create upward movement, negative values create downward movement.
            Defaults to 0 (constant Z).
    
    Returns:
        list: A list of Points representing the variable arc
    
    Example:
        >>> import fullcontrol as fc
        >>> from math import pi, tau
        >>> center = fc.Point(x=50, y=50, z=0)
        >>> # Create a 360° spiral ramp, starting at r=10, ending at r=5, rising by 10mm
        >>> spiral = variable_arcXY(center, 10, 0, tau, 100, -5, 10)
    """
    arc = arcXY(centre, start_radius, start_angle, arc_angle, segments)  # create arc with constant radius and z
    arc = ramp_xyz(arc, z_change=z_change)  # ramp z of the arc
    # ramp radius of the arc
    return ramp_polar(arc, centre, radius_change=radius_change)


def elliptical_arcXY(centre: Point, a: float, b: float, start_angle: float, arc_angle: float, segments: int = 100) -> list:
    """
    Generate a 2D elliptical arc in the XY plane.
    
    This function creates a list of points forming an elliptical arc in the XY plane.
    The Z coordinate of each point will be the same as the Z coordinate of the center point.
    The ellipse is defined by its semi-major axis 'a' and semi-minor axis 'b'.
    Angles are defined in radians.
    
    Args:
        centre (Point): The center point of the elliptical arc
        a (float): The semi-major axis length (X radius) of the ellipse
        b (float): The semi-minor axis length (Y radius) of the ellipse
        start_angle (float): The starting angle in radians
        arc_angle (float): The angular extent of the arc in radians
        segments (int, optional): The number of segments to divide the arc into.
            More segments result in a smoother arc. Defaults to 100.
    
    Returns:
        list: A list of Points representing the elliptical arc
    
    Example:
        >>> import fullcontrol as fc
        >>> from math import pi
        >>> center = fc.Point(x=50, y=50, z=0)
        >>> # Create half of an ellipse with X radius 15 and Y radius 10
        >>> ellipse_arc = elliptical_arcXY(center, 15, 10, 0, pi, 30)
    """
    t_steps = linspace(start_angle, start_angle+arc_angle, segments+1)
    points = [Point(
        x=_clean_float(a*cos(t) + centre.x), 
        y=_clean_float(b*sin(t) + centre.y), 
        z=centre.z
    ) for t in t_steps]
    return points
