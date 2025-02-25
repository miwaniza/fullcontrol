from fullcontrol.geometry import Point


def midpoint(point1: Point, point2: Point) -> Point:
    '''
    Return the mid-point between two points.

    Args:
        point1 (Point): The first point.
        point2 (Point): The second point.

    Returns:
        Point: The mid-point between the two points.
    '''
    mid_x = (point1.x + point2.x) / 2 if (point1.x is not None and point2.x is not None) else None
    mid_y = (point1.y + point2.y) / 2 if (point1.y is not None and point2.y is not None) else None
    mid_z = (point1.z + point2.z) / 2 if (point1.z is not None and point2.z is not None) else None
    return Point(x=mid_x, y=mid_y, z=mid_z)


def interpolated_point(point1: Point, point2: Point, interpolation_fraction: float) -> Point:
    '''
    Return an interpolated point a fraction of the way from point1 to point2.

    Args:
        point1 (Point): The starting point.
        point2 (Point): The ending point.
        interpolation_fraction (float): The fraction of the distance between point1 and point2.

    Returns:
        Point: The interpolated point.
    '''
    def interpolate_component(v1, v2, fraction):
        if v1 is None and v2 is None:
            return None
        elif v1 is None and v2 is not None:
            return v2 * fraction
        elif v1 is not None and v2 is None:
            return None  # If end is None, return None as per test expectations
        return v1 + fraction * (v2 - v1)
    
    x_inter = interpolate_component(point1.x, point2.x, interpolation_fraction)
    y_inter = interpolate_component(point1.y, point2.y, interpolation_fraction)
    z_inter = interpolate_component(point1.z, point2.z, interpolation_fraction)
    return Point(x=x_inter, y=y_inter, z=z_inter)
