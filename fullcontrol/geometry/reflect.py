from fullcontrol.geometry import Point


def reflectXY_axis(p: Point, axis: str = 'x') -> Point:
    '''Return a Point that has been reflected about x=0 (axis='x') or y=0 (axis='y').'''
    p_reflected = Point(x=p.x, y=p.y, z=p.z)
    if axis == 'x':
        p_reflected.y *= -1
    elif axis == 'y':
        p_reflected.x *= -1
    return p_reflected


def reflectXY_mc(p: Point, m_reflect: float, c_reflect: float) -> Point:
    '''Reflects a point about a line y = mx + c.'''
    if m_reflect == 0:  # Horizontal line case
        y_reflect = 2 * c_reflect - p.y
        return Point(x=p.x, y=y_reflect, z=p.z)
    elif abs(m_reflect) == float('inf'):  # Vertical line case
        x_reflect = 2 * c_reflect - p.x
        return Point(x=x_reflect, y=p.y, z=p.z)
    else:
        # For any non-horizontal/non-vertical line:
        # Reflection formula for point (x,y) about line y = mx + c
        # x' = ((1 - m^2)x + 2m(y - c))/(1 + m^2)
        # y' = (2mx - (1 - m^2)y + 2c)/(1 + m^2)
        denom = 1 + m_reflect * m_reflect
        x_reflect = ((1 - m_reflect * m_reflect) * p.x + 2 * m_reflect * (p.y - c_reflect)) / denom
        y_reflect = (2 * m_reflect * p.x - (1 - m_reflect * m_reflect) * p.y + 2 * c_reflect) / denom
        
        return Point(x=x_reflect, y=y_reflect, z=p.z)


def reflectXY(p: Point, p1_reflect: Point, p2_reflect: Point) -> Point:
    '''Reflects a point about a line defined by two points.'''
    # Handle special cases first for better numerical stability
    if abs(p2_reflect.x - p1_reflect.x) < 1e-10:  # Vertical line
        x_reflect = 2 * p1_reflect.x - p.x
        return Point(x=x_reflect, y=p.y, z=p.z)
    elif abs(p2_reflect.y - p1_reflect.y) < 1e-10:  # Horizontal line
        y_reflect = 2 * p1_reflect.y - p.y
        return Point(x=p.x, y=y_reflect, z=p.z)
    else:
        # Calculate line equation y = mx + c
        m_reflect = (p2_reflect.y - p1_reflect.y) / (p2_reflect.x - p1_reflect.x)
        c_reflect = p1_reflect.y - (m_reflect * p1_reflect.x)
        return reflectXY_mc(p, m_reflect, c_reflect)


def reflectXY_points(points, line_point1, line_point2):
    """
    Reflects points across a line defined by two points.
    
    Args:
        points: Points to reflect
        line_point1: First point defining reflection line
        line_point2: Second point defining reflection line
        
    Returns:
        Reflected points
    """
    # Handle both individual points and lists of points
    if hasattr(points, '__iter__') and not isinstance(points, Point):
        return [reflectXY(p, line_point1, line_point2) for p in points]
    else:
        # Handle a single point
        return reflectXY(points, line_point1, line_point2)
