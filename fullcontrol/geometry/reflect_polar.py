from fullcontrol.geometry import Point, polar_to_point
from fullcontrol.geometry.reflect import reflectXY
from math import cos, sin, sqrt

def reflectXYpolar(p: Point, p_reflect: Point, angle_reflect: float) -> Point:
    '''
    Reflects the x and y values of a point about a line defined by a point and polar angle (radians).

    Parameters:
        p (Point): The point to be reflected.
        p_reflect (Point): The point defining the line of reflection.
        angle_reflect (float): The polar angle (radians) of the line of reflection.

    Returns:
        Point: The new point with the original z value.
    '''
    # Create a second point on the reflection line
    # Use exact unit vector components to ensure precise reflection angle
    p2_reflect = Point(
        x=p_reflect.x + round(cos(angle_reflect), 10),  # Round to handle floating point precision
        y=p_reflect.y + round(sin(angle_reflect), 10),
        z=p_reflect.z
    )
    
    return reflectXY(p, p_reflect, p2_reflect)
