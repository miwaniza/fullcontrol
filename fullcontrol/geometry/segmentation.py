from fullcontrol.geometry import Point, interpolated_point, distance
from fullcontrol.common import linspace
from math import sqrt


def segmented_line(point1: Point, point2: Point, segments: int) -> list:
    '''Return equally spaced points along a line segment.'''
    x_steps = linspace(point1.x, point2.x, segments+1)
    y_steps = linspace(point1.y, point2.y, segments+1)
    z_steps = linspace(point1.z, point2.z, segments+1)
    return [Point(x=x_steps[i], y=y_steps[i], z=z_steps[i]) for i in range(segments+1)]


def calculate_cumulative_distances(points: list) -> list:
    """Calculate cumulative distances along a path."""
    distances = [0]
    total = 0
    for i in range(len(points)-1):
        total += distance(points[i], points[i+1])
        distances.append(total)
    return distances


def segmented_path(points: list, segments: int) -> list:
    """
    Calculate a segmented path with equidistant points based on a list of points.
    For curved paths (like circles), this ensures points are equally spaced along the curve.

    Args:
        points (list): A list of points defining the path.
        segments (int): The desired number of segments.

    Returns:
        list: A list of points with equal distances between adjacent points.
    """
    if len(points) < 2:
        return points

    # Calculate cumulative distances along the path
    distances = calculate_cumulative_distances(points)
    total_length = distances[-1]
    if total_length == 0:
        return [points[0]]  # Handle degenerate case

    result = [points[0]]  # Start with first point
    
    # Generate equally spaced points
    for i in range(1, segments):
        target_dist = (i * total_length) / segments
        
        # Find the segment containing target distance
        for j in range(len(distances)-1):
            if distances[j] <= target_dist <= distances[j+1]:
                # Calculate interpolation parameter
                segment_length = distances[j+1] - distances[j]
                t = (target_dist - distances[j]) / segment_length if segment_length > 0 else 0
                # Add interpolated point
                new_point = interpolated_point(points[j], points[j+1], t)
                result.append(new_point)
                break
    
    result.append(points[-1])  # Add final point
    return result
