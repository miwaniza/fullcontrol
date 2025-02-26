from fullcontrol.geometry import Point, Vector, point_to_polar, polar_to_point, move, move_polar
from math import pi, tau, sin, cos, atan2


def squarewaveXYpolar(start_point: Point, direction_polar: float, amplitude: float, line_spacing: float, periods: int, extra_half_period: bool = False, extra_end_line: bool = False) -> list:
    '''Generate a squarewave with the set number of periods, starting at the start_point.'''
    steps = []
    current = start_point.copy()
    steps.append(current)

    for i in range(periods):
        # Up
        current = polar_to_point(centre=current, radius=amplitude, angle=direction_polar + pi/2)
        steps.append(current)
        
        # Right (half line_spacing)
        current = polar_to_point(centre=current, radius=line_spacing/2, angle=direction_polar)
        steps.append(current)
        
        # Down
        current = polar_to_point(centre=current, radius=2*amplitude, angle=direction_polar - pi/2)
        steps.append(current)
        
        # Right (half line_spacing)
        current = polar_to_point(centre=current, radius=line_spacing/2, angle=direction_polar)
        steps.append(current)

    if extra_half_period:
        # Up for half period
        current = polar_to_point(centre=current, radius=amplitude, angle=direction_polar + pi/2)
        steps.append(current)
        
        # Optional extra line at end
        if extra_end_line:
            current = polar_to_point(centre=current, radius=line_spacing/2, angle=direction_polar)
            steps.append(current)

    return steps


def squarewaveXY(start_point: Point, direction_vector: Vector, amplitude: float, line_spacing: float, periods: int, extra_half_period: bool = False, extra_end_line: bool = False) -> list:
    '''Generate a square wave using a direction vector instead of polar angle.'''
    if direction_vector.x == None:
        direction_vector.x = 0
    if direction_vector.y == None:
        direction_vector.y = 0
    direction_polar = atan2(direction_vector.y, direction_vector.x)
    return squarewaveXYpolar(start_point, direction_polar, amplitude, line_spacing, periods, extra_half_period, extra_end_line)


def trianglewaveXYpolar(start_point: Point, direction_polar: float, amplitude: float, tip_separation: float, periods: int, extra_half_period: bool = False) -> list:
    '''Generate a triangle wave with given parameters.'''
    steps = []
    current = start_point.copy()
    steps.append(current)

    for i in range(periods):
        # Up to peak
        current = polar_to_point(centre=current, radius=amplitude, angle=direction_polar + pi/2)
        steps.append(current)
        
        # Down and right to valley
        valley = polar_to_point(centre=current, radius=2*amplitude, angle=direction_polar - pi/2)
        current = polar_to_point(centre=valley, radius=tip_separation, angle=direction_polar)
        steps.append(current)
        
        # For all but last period, return to midpoint to start next period
        if i < periods - 1:
            current = polar_to_point(centre=current, radius=amplitude, angle=direction_polar + pi/2)
            steps.append(current)

    # Add half period if requested (move right half distance, then up)
    if extra_half_period:
        # Move right half tip separation
        current = polar_to_point(centre=current, radius=tip_separation/2, angle=direction_polar)
        steps.append(current)
        # Move up to complete half period
        current = polar_to_point(centre=current, radius=amplitude, angle=direction_polar + pi/2)
        steps.append(current)

    return steps


def sinewaveXYpolar(start_point: Point, direction_polar: float, amplitude: float, period_length: float, periods: int, segments_per_period: int = 16, extra_half_period: bool = False, phase_shift: float = 0) -> list:
    '''Generate a sine wave with given parameters.'''
    steps = []
    
    # Calculate total number of segments
    total_segments = segments_per_period * periods
    if extra_half_period:
        total_segments += segments_per_period // 2
        
    # Generate points along the wave
    for i in range(total_segments + 1):
        t = i / segments_per_period  # Position in periods
        angle = 2 * pi * t + phase_shift  # Angle for sine calculation
        
        # Calculate local coordinates (before rotation)
        local_x = t * period_length
        local_y = amplitude * sin(angle)
        
        # Transform to global coordinates using rotation matrix
        global_x = start_point.x + local_x * cos(direction_polar) - local_y * sin(direction_polar)
        global_y = start_point.y + local_x * sin(direction_polar) + local_y * cos(direction_polar)
        
        steps.append(Point(x=global_x, y=global_y, z=start_point.z))
    
    return steps
