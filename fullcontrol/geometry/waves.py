from typing import List, Optional
from fullcontrol.combinations.gcode_and_visualize.classes import Point
from fullcontrol.geometry.vector import Vector 
from fullcontrol.geometry.rotate import normalize_vector
from math import sin, cos, pi, tau

def round_near_zero(value: float, tolerance: float = 1e-10) -> float:
    """Round values very close to zero to exactly zero."""
    return 0.0 if abs(value) < tolerance else value

def squarewaveXY(start: Point, direction: Vector, amplitude: float, line_spacing: float, 
                periods: int, extra_half_period: bool = False) -> List[Point]:
    """Generate a square wave in XY plane."""
    # Normalize direction vector
    unit_dir = normalize_vector(direction)
    
    # Create perpendicular vector for amplitude
    ampl_dir = Vector(x=-unit_dir.y, y=unit_dir.x)  # Rotate 90 degrees CCW
    
    points = [start]  # Start point
    
    for i in range(periods):
        # Up
        points.append(Point(
            x=round_near_zero(points[-1].x + ampl_dir.x * amplitude),
            y=round_near_zero(points[-1].y + ampl_dir.y * amplitude),
            z=points[-1].z
        ))
        # Right
        points.append(Point(
            x=round_near_zero(points[-1].x + unit_dir.x * line_spacing),
            y=round_near_zero(points[-1].y + unit_dir.y * line_spacing),
            z=points[-1].z
        ))
        # Down
        points.append(Point(
            x=round_near_zero(points[-1].x - ampl_dir.x * 2 * amplitude),
            y=round_near_zero(points[-1].y - ampl_dir.y * 2 * amplitude),
            z=points[-1].z
        ))
        # Right
        points.append(Point(
            x=round_near_zero(points[-1].x + unit_dir.x * line_spacing),
            y=round_near_zero(points[-1].y + unit_dir.y * line_spacing),
            z=points[-1].z
        ))
    
    # Add final up move for extra half period
    if extra_half_period:
        points.append(Point(
            x=round_near_zero(points[-1].x + ampl_dir.x * 2 * amplitude),
            y=round_near_zero(points[-1].y + ampl_dir.y * 2 * amplitude),
            z=points[-1].z
        ))
    
    return points

def squarewaveXYpolar(start: Point, direction_polar: float, amplitude: float, line_spacing: float,
                      periods: int, extra_half_period: bool = False) -> List[Point]:
    """Generate a square wave using polar direction."""
    direction = Vector(x=cos(direction_polar), y=sin(direction_polar))
    return squarewaveXY(start, direction, amplitude, line_spacing, periods, extra_half_period)

def trianglewaveXYpolar(start: Point, direction_polar: float, amplitude: float, tip_separation: float,
                       periods: int) -> List[Point]:
    """Generate a triangle wave using polar direction."""
    direction = Vector(x=cos(direction_polar), y=sin(direction_polar))
    unit_dir = normalize_vector(direction)
    
    # Create perpendicular vector for amplitude
    ampl_dir = Vector(x=-unit_dir.y, y=unit_dir.x)
    
    points = [start]
    
    for i in range(periods):
        # Up to positive peak
        points.append(Point(
            x=round_near_zero(points[-1].x),
            y=round_near_zero(points[-1].y + amplitude),
            z=points[-1].z
        ))
        # Down to negative peak with forward movement
        points.append(Point(
            x=round_near_zero(points[-1].x + tip_separation),
            y=round_near_zero(points[-1].y - 2 * amplitude),
            z=points[-1].z
        ))
        # Back to baseline with forward movement
        points.append(Point(
            x=round_near_zero(points[-1].x + tip_separation),
            y=round_near_zero(points[-1].y + amplitude),
            z=points[-1].z
        ))
    
    return points

def sinewaveXYpolar(start: Point, direction_polar: float, amplitude: float, period_length: float,
                    periods: int, segments_per_period: int = 32, phase_shift: float = 0) -> List[Point]:
    """Generate a sine wave using polar direction."""
    points = []
    
    # Calculate points along the sine wave
    for i in range(segments_per_period * periods + 1):
        t = i * (2 * pi) / segments_per_period  # Convert to radians
        x = start.x + (t / (2 * pi)) * period_length
        y = start.y + amplitude * sin(t + phase_shift)
        
        points.append(Point(
            x=round_near_zero(x),
            y=round_near_zero(y),
            z=start.z
        ))
    
    return points
