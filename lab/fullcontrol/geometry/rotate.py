import math
from fullcontrol.geometry import Point
from typing import Union
from copy import deepcopy
from math import sqrt, cos, sin, radians


def dot_product(v1, v2):
    """Calculate dot product between two vectors, treating None components as 0."""
    result = 0
    if v1.x is not None and v2.x is not None:
        result += v1.x * v2.x
    if v1.y is not None and v2.y is not None:
        result += v1.y * v2.y
    if v1.z is not None and v2.z is not None:
        result += v1.z * v2.z
    return result


def cross_product(v1, v2):
    """Calculate cross product between two vectors, treating None components as 0."""
    x1, y1, z1 = v1.x or 0, v1.y or 0, v1.z or 0
    x2, y2, z2 = v2.x or 0, v2.y or 0, v2.z or 0
    return Point(
        x=y1*z2 - z1*y2,
        y=z1*x2 - x1*z2,
        z=x1*y2 - y1*x2
    )


def rotate(geometry: Union[Point, list], axis_start: Point, axis_end_or_direction: Union[Point, str], angle_rad: float, copy: bool = False, copy_quantity: int = 2) -> Union[Point, list]:
    '''rotate 'geometry' (a Point or list of steps including Points)
    about the given axis by the given angle and return the rotated
    geometry (original geometry is not edited). Non-Point elements in
    a list pass through without modification.

    Args:
        geometry (Union[Point, list]): The geometry to rotate - a Point or list of Points/steps
        axis_start (Point): Starting point of the rotation axis
        axis_end_or_direction (Union[Point, str]): End point of rotation axis or direction ('x', 'y', 'z')
        angle_rad (float): Angle in radians
        copy (bool, optional): Whether to create multiple copies. Defaults to False.
        copy_quantity (int, optional): Number of copies if copy=True. Defaults to 2.

    Returns:
        Union[Point, list]: The rotated geometry
    '''
    # Handle string direction
    if isinstance(axis_end_or_direction, str):
        axis_end = Point(
            x=axis_start.x + (1 if axis_end_or_direction == 'x' else 0),
            y=axis_start.y + (1 if axis_end_or_direction == 'y' else 0),
            z=axis_start.z + (1 if axis_end_or_direction == 'z' else 0)
        )
    else:
        axis_end = axis_end_or_direction

    if copy:
        return rotate_copy_geometry(geometry, axis_start, axis_end, angle_rad, copy_quantity)
    else:
        return rotate_geometry(geometry, axis_start, axis_end, angle_rad)


def rotate_geometry(geometry: Union[Point, list], axis_start: Point, axis_end: Point, angle_rad: float) -> Union[Point, list]:
    '''rotate 'geometry' (a Point or list of steps including Points) 
    about the given axis by the given angle' and return the rotated 
    geometry (original geometry is not edited). elements in a list. 
    Objects that are not Points pass through without modification
    '''

    def rotate_point(point: Point, axis_start: Point, axis_end: Point, angle_rad: float) -> Point:
        'return a copy of a the given point, rotated about the given axis by the given angle'
        point_new = deepcopy(point)  # deepcopy so that color attribute is copied

        # Vector along the rotation axis
        axis = Point(x=axis_end.x - axis_start.x, y=axis_end.y - axis_start.y, z=axis_end.z - axis_start.z)

        # Normalize the rotation axis vector
        norm = sqrt(axis.x**2 + axis.y**2 + axis.z**2)
        axis = Point(x=axis.x/norm, y=axis.y/norm, z=axis.z/norm)

        # offset to be relative to origin
        point_new.x -= axis_start.x
        point_new.y -= axis_start.y
        point_new.z -= axis_start.z

        # Rotation using Rodriguez rotation formula
        cos_theta = cos(angle_rad)
        sin_theta = sin(angle_rad)

        # dot product with rotation axis
        dot = dot_product(point_new, axis)
        # cross product with rotation axis
        cross = cross_product(axis, point_new)
        
        # rotate the point
        x = point_new.x*cos_theta + cross.x*sin_theta + axis.x*dot*(1-cos_theta)
        y = point_new.y*cos_theta + cross.y*sin_theta + axis.y*dot*(1-cos_theta)
        z = point_new.z*cos_theta + cross.z*sin_theta + axis.z*dot*(1-cos_theta)

        # restore offset position
        x += axis_start.x
        y += axis_start.y
        z += axis_start.z

        return Point(x=x, y=y, z=z)

    if isinstance(geometry, Point):
        return rotate_point(geometry, axis_start, axis_end, angle_rad)
    else:
        geometry_new = []
        for element in geometry:
            if isinstance(element, Point):
                geometry_new.append(rotate_point(element, axis_start, axis_end, angle_rad))
            else:
                geometry_new.append(element)
        return geometry_new


def rotate_copy_geometry(geometry: Union[Point, list], axis_start: Point, axis_end: Point, angle_rad: float, quantity: int) -> list:
    '''creates multiple copies of 'geometry' (a Point or list of steps including
    Points), each rotated about the given axis by the given angle. elements in a list
    that are not Points pass through and are replicated without modification.
    'quantity' includes the position of the original geometry. return the new
    geometry as a list (original geometry is not edited).
    '''
    steps_new = []
    for i in range(quantity):
        angle_now = angle_rad*i
        if isinstance(geometry, Point):
            steps_new.append(rotate_geometry(geometry, axis_start, axis_end, angle_now))
        else:
            steps_new.extend(rotate_geometry(geometry, axis_start, axis_end, angle_now))
    return steps_new
