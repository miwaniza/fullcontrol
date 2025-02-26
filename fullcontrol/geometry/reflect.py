from fullcontrol.geometry import Point, Vector
from typing import Union, List
import math

def round_near_zero(value: float, tolerance: float = 1e-10) -> float:
    """Round values very close to zero to exactly zero."""
    return 0.0 if abs(value) < tolerance else value

def reflectXY_mc(p: Point, m_reflect: float, c_reflect: float) -> Point:
    '''Reflects a point about a line y = mx + c.
    
    The reflection formula for point (h,k) about line y = mx + c is:
    x = ((1-m^2)h + 2m(k-c)) / (1+m^2)
    y = (2mh - (1-m^2)k + 2c) / (1+m^2)
    '''
    # Handle special cases with better numerical stability
    if abs(m_reflect) < 1e-10:  # Horizontal line case
        y_reflect = 2 * c_reflect - p.y
        return Point(x=p.x, y=round_near_zero(y_reflect), z=p.z)
    elif abs(m_reflect) > 1e10:  # Vertical line case
        x_reflect = 2 * c_reflect - p.x
        return Point(x=round_near_zero(x_reflect), y=p.y, z=p.z)
    else:
        # For y = mx + c line, using standard reflection formula
        denom = 1 + m_reflect * m_reflect
        x_reflect = ((1 - m_reflect * m_reflect) * p.x + 2 * m_reflect * (p.y - c_reflect)) / denom
        y_reflect = (2 * m_reflect * p.x - (1 - m_reflect * m_reflect) * p.y + 2 * c_reflect) / denom
        
        # Round values very close to zero
        x_reflect = round_near_zero(x_reflect)
        y_reflect = round_near_zero(y_reflect)
        
        return Point(x=x_reflect, y=y_reflect, z=p.z)

def reflectXY_axis(p: Point, axis: str = 'x') -> Point:
    '''Return a Point that has been reflected about x=0 (axis='x') or y=0 (axis='y').'''
    p_reflected = Point(x=p.x, y=p.y, z=p.z)
    if axis == 'x':
        p_reflected.y *= -1
    elif axis == 'y':
        p_reflected.x *= -1
    return p_reflected

def reflectXY(p: Point, p1_reflect: Point, p2_reflect: Point) -> Point:
    '''Reflects a point about a line defined by two points.'''
    # Handle special cases first for better numerical stability
    if abs(p2_reflect.x - p1_reflect.x) < 1e-10:  # Vertical line
        x_reflect = 2 * p1_reflect.x - p.x
        return Point(x=round_near_zero(x_reflect), y=p.y, z=p.z)
    elif abs(p2_reflect.y - p1_reflect.y) < 1e-10:  # Horizontal line
        y_reflect = 2 * p1_reflect.y - p.y
        return Point(x=p.x, y=round_near_zero(y_reflect), z=p.z)
    else:
        # Calculate line equation y = mx + c
        m_reflect = (p2_reflect.y - p1_reflect.y) / (p2_reflect.x - p1_reflect.x)
        c_reflect = p1_reflect.y - (m_reflect * p1_reflect.x)
        return reflectXY_mc(p, m_reflect, c_reflect)

def reflectXY_points(points: Union[Point, List[Point]], line_point1: Point, line_point2: Point) -> Union[Point, List[Point]]:
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
