from fullcontrol.geometry import Point, point_to_polar
from math import tau, pi


def distance(point1: Point, point2: Point) -> float:
    '''Calculate the Euclidean distance between two points in 3D space.'''
    return ((point1.x-point2.x)**2+(point1.y-point2.y)**2+(point1.z-point2.z)**2)**0.5


def distance_forgiving(point1: Point, point2: Point) -> float:
    '''Calculate the distance between two points, ignoring undefined components.'''
    dist_x = 0 if point1.x == None or point2.x == None else point1.x - point2.x
    dist_y = 0 if point1.y == None or point2.y == None else point1.y - point2.y
    dist_z = 0 if point1.z == None or point2.z == None else point1.z - point2.z
    return ((dist_x)**2+(dist_y)**2+(dist_z)**2)**0.5


def angleXY_between_3_points(start_point: Point, mid_point: Point, end_point: Point) -> float:
    '''
    Returns the angle from start_point to end_point, about mid_point.
    The angle is returned in radians between 0 and π.

    Parameters:
    start_point (Point): The starting point.
    mid_point (Point): The middle point (vertex).
    end_point (Point): The ending point.

    Returns:
    float: The angle in radians between 0 and π.
    '''
    # Get the angles in polar coordinates
    end_polar = point_to_polar(end_point, mid_point)
    start_polar = point_to_polar(start_point, mid_point)
    
    # Calculate angle difference
    diff = end_polar.angle - start_polar.angle
    
    # Normalize to [0, tau)
    while diff < 0:
        diff += tau
    while diff >= tau:
        diff -= tau
        
    # Convert to [0, pi] range
    if diff > pi:
        diff = tau - diff
        
    return diff


def path_length(points: list) -> float:
    """Calculates the total length of a path defined by a list of points."""
    return sum([distance(points[i], points[i+1]) for i in range(len(points)-1)])
