from fullcontrol.geometry import Point, polar_to_point
from fullcontrol.geometry.reflect import reflectXY_points

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
    # Create second point on reflection line using polar coordinates
    p2_reflect = polar_to_point(p_reflect, 1, angle_reflect)
    return reflectXY_points(p, p_reflect, p2_reflect)
