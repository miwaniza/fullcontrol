from typing import Union, List
from math import cos, sin
from fullcontrol.geometry.vector import Vector

def rotate_vector(v: Vector, angle: float) -> Vector:
    """Rotate a vector by an angle (in radians)."""
    return Vector(
        x=v.x * cos(angle) - v.y * sin(angle),
        y=v.x * sin(angle) + v.y * cos(angle)
    )

def normalize_vector(v: Vector) -> Vector:
    """Normalize a vector to unit length."""
    length = (v.x * v.x + v.y * v.y) ** 0.5
    if abs(length) < 1e-10:
        return Vector(x=0, y=0)
    return Vector(x=v.x/length, y=v.y/length)