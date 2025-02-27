from fullcontrol.geometry import Point, arcXY, variable_arcXY, elliptical_arcXY
from math import tau


def rectangleXY(start_point: Point, x_size: float, y_size: float, cw: bool = False) -> list:
    """
    Generate a 2D rectangle in the XY plane.
    
    Creates a rectangular path starting and ending at the given point, moving in either
    clockwise or counter-clockwise direction. The function returns 5 points, including
    the duplicated start point at the end to form a closed shape.
    
    Args:
        start_point (Point): The starting (and ending) point of the rectangle
        x_size (float): The width of the rectangle along the X-axis
        y_size (float): The height of the rectangle along the Y-axis
        cw (bool, optional): Direction of points generation.
            If True, generates clockwise: start → right → up → left → start
            If False, generates counter-clockwise: start → up → right → down → start
            Defaults to False.
    
    Returns:
        list: A list of five Points representing the rectangle, with the first point
            repeated at the end to create a closed path
    
    Example:
        >>> import fullcontrol as fc
        >>> rect = rectangleXY(fc.Point(x=0, y=0, z=0), 20, 10)
        >>> # Creates a 20mm × 10mm rectangle starting at origin
    """
    if cw:
        # Clockwise: start → right → up → left → start
        point1 = Point(x=start_point.x + x_size, y=start_point.y, z=start_point.z)
        point2 = Point(x=start_point.x + x_size, y=start_point.y + y_size, z=start_point.z)
        point3 = Point(x=start_point.x, y=start_point.y + y_size, z=start_point.z)
    else:
        # Counter-clockwise: start → up → right → down → start
        point1 = Point(x=start_point.x, y=start_point.y + y_size, z=start_point.z)
        point2 = Point(x=start_point.x + x_size, y=start_point.y + y_size, z=start_point.z)
        point3 = Point(x=start_point.x + x_size, y=start_point.y, z=start_point.z)
    return [start_point.model_copy(), point1, point2, point3, start_point.model_copy()]


def circleXY(centre: Point, radius: float, start_angle: float, segments: int = 100, cw: bool = False) -> list:
    """
    Generate a 2D circle in the XY plane.
    
    Creates a circular path centered at the given point with the specified radius.
    The circle starts at the specified angle and proceeds in the requested direction.
    The Z coordinate remains constant at the value from the center point.
    
    Args:
        centre (Point): The center point of the circle
        radius (float): The radius of the circle
        start_angle (float): The starting angle in radians
        segments (int, optional): The number of segments to divide the circle into.
            Higher values create a smoother circle. Defaults to 100.
        cw (bool, optional): Direction of circle generation.
            If True, generates clockwise.
            If False, generates counter-clockwise.
            Defaults to False.
    
    Returns:
        list: A list of Points representing the circle
    
    Example:
        >>> import fullcontrol as fc
        >>> from math import pi
        >>> # Create a circle with radius 5mm at Z=0.2mm, starting from angle 0
        >>> circ = circleXY(fc.Point(x=10, y=10, z=0.2), 5, 0)
    """
    return arcXY(centre, radius, start_angle, tau*(1-(2*cw)), segments)


def circleXY_3pt(pt1: Point, pt2: Point, pt3: Point, start_angle: float, segments: int = 100, cw: bool = False) -> list:
    """
    Generate a 2D circle passing through three specified points.
    
    Creates a circle that passes through the three given points. This is useful when
    the center of the circle is not known, but three points on the circumference are.
    The Z coordinate is taken from the first point and remains constant.
    
    Args:
        pt1 (Point): First point on the circle's circumference
        pt2 (Point): Second point on the circle's circumference
        pt3 (Point): Third point on the circle's circumference
        start_angle (float): The starting angle in radians for generating the circle
        segments (int, optional): The number of segments to divide the circle into.
            Higher values create a smoother circle. Defaults to 100.
        cw (bool, optional): Direction of circle generation.
            If True, generates clockwise.
            If False, generates counter-clockwise.
            Defaults to False.
    
    Returns:
        list: A list of Points representing the circle
    
    Raises:
        Exception: If the three points are collinear (lie on a straight line),
            meaning no unique circle can pass through them
    
    Example:
        >>> import fullcontrol as fc
        >>> # Create a circle passing through three points
        >>> p1 = fc.Point(x=0, y=0, z=0)
        >>> p2 = fc.Point(x=10, y=0, z=0)
        >>> p3 = fc.Point(x=5, y=8, z=0)
        >>> circle = circleXY_3pt(p1, p2, p3, 0)
    """
    D = 2 * (pt1.x * (pt2.y - pt3.y) + pt2.x * (pt3.y - pt1.y) + pt3.x * (pt1.y - pt2.y))
    if D == 0:
        raise Exception('The points are collinear, no unique circle')
    x_centre = ((pt1.x**2 + pt1.y**2) * (pt2.y - pt3.y) + (pt2.x**2 + pt2.y**2) * (pt3.y - pt1.y) + (pt3.x**2 + pt3.y**2) * (pt1.y - pt2.y)) / D
    y_centre = ((pt1.x**2 + pt1.y**2) * (pt3.x - pt2.x) + (pt2.x**2 + pt2.y**2) * (pt1.x - pt3.x) + (pt3.x**2 + pt3.y**2) * (pt2.x - pt1.x)) / D
    radius = ((pt1.x - x_centre)**2 + (pt1.y - y_centre)**2)**0.5
    centre = Point(x=x_centre, y=y_centre, z=pt1.z)
    return arcXY(centre, radius, start_angle, tau*(1-(2*cw)), segments)


def ellipseXY(centre: Point, a: float, b: float, start_angle: float, segments: int = 100, cw: bool = False) -> list:
    """
    Generate a 2D ellipse in the XY plane.
    
    Creates an elliptical path centered at the given point with the specified
    semi-major (a) and semi-minor (b) axes. The ellipse starts at the specified 
    angle and proceeds in the requested direction. The Z coordinate remains 
    constant at the value from the center point.
    
    Args:
        centre (Point): The center point of the ellipse
        a (float): The semi-major axis length (width/2) of the ellipse
        b (float): The semi-minor axis length (height/2) of the ellipse
        start_angle (float): The starting angle in radians
        segments (int, optional): The number of segments to divide the ellipse into.
            Higher values create a smoother ellipse. Defaults to 100.
        cw (bool, optional): Direction of ellipse generation.
            If True, generates clockwise.
            If False, generates counter-clockwise.
            Defaults to False.
    
    Returns:
        list: A list of Points representing the ellipse
    
    Example:
        >>> import fullcontrol as fc
        >>> # Create an ellipse with semi-major axis 15mm and semi-minor axis 10mm
        >>> ellipse = ellipseXY(fc.Point(x=50, y=50, z=0), 15, 10, 0)
    """
    return elliptical_arcXY(centre, a, b, start_angle, tau*(1-(2*cw)), segments)


def polygonXY(centre: Point, enclosing_radius: float, start_angle: float, sides: int, cw: bool = False) -> list:
    """
    Generate a regular polygon in the XY plane.
    
    Creates a regular polygon with the specified number of sides. The polygon is
    centered at the given point and all vertices lie on a circle with the specified
    enclosing radius. The first vertex is positioned at the start angle.
    
    Args:
        centre (Point): The center point of the polygon
        enclosing_radius (float): The radius of the circle on which all vertices lie
        start_angle (float): The angle in radians for the first vertex
        sides (int): The number of sides of the polygon
        cw (bool, optional): Direction of polygon generation.
            If True, generates clockwise.
            If False, generates counter-clockwise.
            Defaults to False.
    
    Returns:
        list: A list of Points representing the polygon vertices, with the first
            point repeated at the end to create a closed path
    
    Example:
        >>> import fullcontrol as fc
        >>> # Create a hexagon with radius 10mm
        >>> hexagon = polygonXY(fc.Point(x=0, y=0, z=0), 10, 0, 6)
    """
    return arcXY(centre, enclosing_radius, start_angle, tau*(1-(2*cw)), sides)  # cw parameter used to achieve +1 or -1


def spiralXY(centre: Point, start_radius: float, end_radius: float, start_angle: float, n_turns: float, segments: int, cw: bool = False) -> list:
    """
    Generate a 2D spiral in the XY plane.
    
    Creates a spiral path that starts at the specified radius and angle, and
    gradually changes to the end radius over the specified number of turns.
    The Z coordinate remains constant at the value from the center point.
    
    Args:
        centre (Point): The center point of the spiral
        start_radius (float): The radius at the beginning of the spiral
        end_radius (float): The radius at the end of the spiral
        start_angle (float): The starting angle in radians
        n_turns (float): The number of complete turns (can be fractional)
        segments (int): The number of segments to divide the spiral into
        cw (bool, optional): Direction of spiral generation.
            If True, generates clockwise.
            If False, generates counter-clockwise.
            Defaults to False.
    
    Returns:
        list: A list of Points representing the spiral
    
    Example:
        >>> import fullcontrol as fc
        >>> from math import tau
        >>> # Create a 2-turn spiral from radius 20mm to 5mm
        >>> spiral = spiralXY(fc.Point(x=50, y=50, z=0), 20, 5, 0, 2, 100)
    """
    return variable_arcXY(centre, start_radius, start_angle, arc_angle=n_turns*tau*(1-(2*cw)), segments=segments, radius_change=end_radius-start_radius, z_change=0)


def helixZ(centre: Point, start_radius: float, end_radius: float, start_angle: float, n_turns: float, pitch_z: float, segments: int, cw: bool = False) -> list:
    """
    Generate a helical path along the Z axis.
    
    Creates a 3D helix that rises along the Z axis while simultaneously spiraling
    in the XY plane. The helix can have a varying radius, changing from start_radius
    to end_radius over the specified number of turns.
    
    Args:
        centre (Point): The center point of the helix base
        start_radius (float): The radius at the beginning of the helix
        end_radius (float): The radius at the end of the helix
        start_angle (float): The starting angle in radians
        n_turns (float): The number of complete turns (can be fractional)
        pitch_z (float): The vertical distance traveled per complete turn
        segments (int): The number of segments to divide the helix into
        cw (bool, optional): Direction of helix generation in the XY plane.
            If True, generates clockwise.
            If False, generates counter-clockwise.
            Defaults to False.
    
    Returns:
        list: A list of Points representing the helical path
    
    Example:
        >>> import fullcontrol as fc
        >>> # Create a 3-turn helix with constant radius 10mm and 5mm pitch
        >>> helix = helixZ(fc.Point(x=0, y=0, z=0), 10, 10, 0, 3, 5, 120)
        >>> # Final Z height will be 15mm (3 turns × 5mm pitch)
    """
    return variable_arcXY(centre, start_radius, start_angle, arc_angle=n_turns*tau*(1-(2*cw)), segments=segments, radius_change=end_radius-start_radius, z_change=pitch_z*n_turns)
