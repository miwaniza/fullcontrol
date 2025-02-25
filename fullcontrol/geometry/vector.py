from typing import Optional, Union, Any
from math import sqrt, acos, pi
from pydantic import BaseModel
from fullcontrol.geometry import Point


class Vector(BaseModel):
    """A 3D vector class supporting basic vector operations."""
    x: Optional[float] = None
    y: Optional[float] = None
    z: Optional[float] = None

    @classmethod
    def from_points(cls, p1: Point, p2: Point) -> 'Vector':
        """Create a vector from two points."""
        return cls(
            x=p2.x - p1.x if p1.x is not None and p2.x is not None else None,
            y=p2.y - p1.y if p1.y is not None and p2.y is not None else None,
            z=p2.z - p1.z if p1.z is not None and p2.z is not None else None
        )

    def __add__(self, other: 'Vector') -> 'Vector':
        """Add two vectors."""
        return Vector(
            x=self.x + other.x if self.x is not None and other.x is not None else None,
            y=self.y + other.y if self.y is not None and other.y is not None else None,
            z=self.z + other.z if self.z is not None and other.z is not None else None
        )

    def __sub__(self, other: 'Vector') -> 'Vector':
        """Subtract two vectors."""
        return Vector(
            x=self.x - other.x if self.x is not None and other.x is not None else None,
            y=self.y - other.y if self.y is not None and other.y is not None else None,
            z=self.z - other.z if self.z is not None and other.z is not None else None
        )

    def __mul__(self, scalar: Union[int, float]) -> 'Vector':
        """Multiply vector by scalar."""
        return Vector(
            x=self.x * scalar if self.x is not None else None,
            y=self.y * scalar if self.y is not None else None,
            z=self.z * scalar if self.z is not None else None
        )

    def __rmul__(self, scalar: Union[int, float]) -> 'Vector':
        """Right multiplication by scalar."""
        return self * scalar

    def __truediv__(self, scalar: Union[int, float]) -> 'Vector':
        """Divide vector by scalar."""
        return Vector(
            x=self.x / scalar if self.x is not None else None,
            y=self.y / scalar if self.y is not None else None,
            z=self.z / scalar if self.z is not None else None
        )

    def dot(self, other: 'Vector') -> float:
        """Calculate dot product with another vector."""
        components = []
        if self.x is not None and other.x is not None:
            components.append(self.x * other.x)
        if self.y is not None and other.y is not None:
            components.append(self.y * other.y)
        if self.z is not None and other.z is not None:
            components.append(self.z * other.z)
        return sum(components)

    def cross(self, other: 'Vector') -> 'Vector':
        """Calculate cross product with another vector."""
        # Handle None values by treating them as 0
        x1, y1, z1 = self.x or 0, self.y or 0, self.z or 0
        x2, y2, z2 = other.x or 0, other.y or 0, other.z or 0
        
        return Vector(
            x=y1*z2 - z1*y2,
            y=z1*x2 - x1*z2,
            z=x1*y2 - y1*x2
        )

    def magnitude(self) -> float:
        """Calculate the magnitude (length) of the vector."""
        components = []
        if self.x is not None:
            components.append(self.x * self.x)
        if self.y is not None:
            components.append(self.y * self.y)
        if self.z is not None:
            components.append(self.z * self.z)
        return sqrt(sum(components))

    def normalize(self) -> 'Vector':
        """Return a normalized version of the vector."""
        mag = self.magnitude()
        if mag == 0:
            return Vector(x=0, y=0, z=0)
        return self / mag

    def angle(self, other: 'Vector') -> float:
        """Calculate the angle between this vector and another vector in radians."""
        # Handle zero vectors
        if self.magnitude() == 0 or other.magnitude() == 0:
            return 0.0
        
        # Calculate cosine using dot product
        cos_angle = self.dot(other) / (self.magnitude() * other.magnitude())
        
        # Handle floating point errors
        if cos_angle > 1:
            cos_angle = 1
        elif cos_angle < -1:
            cos_angle = -1
            
        return acos(cos_angle)

    @classmethod
    def unit_x(cls) -> 'Vector':
        """Return a unit vector in the x direction."""
        return cls(x=1, y=0, z=0)

    @classmethod
    def unit_y(cls) -> 'Vector':
        """Return a unit vector in the y direction."""
        return cls(x=0, y=1, z=0)

    @classmethod
    def unit_z(cls) -> 'Vector':
        """Return a unit vector in the z direction."""
        return cls(x=0, y=0, z=1)
