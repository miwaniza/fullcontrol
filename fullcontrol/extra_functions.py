from fullcontrol.common import Point
from itertools import chain
from copy import deepcopy
from typing import Union


def points_only(steps: list, track_xyz: bool = True) -> list:
    """
    Converts a list of mixed steps to a list containing only Point objects.
    
    This function extracts only Point objects from a list of steps that may contain
    both Points and control data. When track_xyz is True, it also handles coordinate
    inheritance between consecutive points to ensure continuity.
    
    Args:
        steps (list): A list of steps containing Points and control data.
        track_xyz (bool, optional): Specifies whether to track the xyz values of the Points. 
            If True, returns only the first fully defined point and the point immediately after it,
            with undefined values in the second point inherited from the first point.
            If False, the Points are returned as they are defined, including attributes with value=None.
    
    Returns:
        list: A new list containing only Points.
    
    Example:
        >>> import fullcontrol as fc
        >>> steps = [fc.Point(x=0, y=0, z=0), fc.Extruder(on=True), fc.Point(x=10, y=None, z=None)]
        >>> points = points_only(steps)
        >>> print(len(points), points[1].y, points[1].z)  # Will show: 2 0 0
    """
    # First collect only Point instances
    new_steps = []
    for step in steps:
        if isinstance(step, Point):  # only consider Point data
            new_steps.append(deepcopy(step))
    
    if track_xyz and new_steps:
        # Find the first fully defined point
        start_idx = None
        for i, point in enumerate(new_steps):
            if point.x is not None and point.y is not None and point.z is not None:
                start_idx = i
                break
        
        if start_idx is not None and start_idx + 1 < len(new_steps):
            result = new_steps[start_idx:start_idx + 2]
            # Make second point inherit undefined values from first point
            if result[1].x is None:
                result[1].x = result[0].x
            if result[1].y is None:
                result[1].y = result[0].y
            if result[1].z is None:
                result[1].z = result[0].z
            return result
        elif start_idx is not None:
            return [new_steps[start_idx]]
        return []

    return new_steps


def relative_point(reference: Union[Point, list], x_offset: float, y_offset: float, z_offset: float):
    """
    Creates a new Point with position relative to a reference point.
    
    This function generates a new Point by applying specified offsets to a reference
    point's coordinates. The reference can be either a single Point object or a list
    from which the last Point will be used as reference.
    
    Args:
        reference (Union[Point, list]): The reference point or a list of points. If a list is supplied, 
                                        the last point in the list is used as the reference point.
        x_offset (float): The offset in the x-axis.
        y_offset (float): The offset in the y-axis.
        z_offset (float): The offset in the z-axis.
    
    Returns:
        Point: A new Point object with coordinates offset from the reference point.
    
    Raises:
        Exception: If the reference object is not a Point or a list containing at least one point.
        Exception: If the reference point does not have all of x, y, z attributes defined.
    
    Example:
        >>> import fullcontrol as fc
        >>> base_point = fc.Point(x=10, y=20, z=30)
        >>> new_point = relative_point(base_point, 5, -10, 0)
        >>> print(new_point.x, new_point.y, new_point.z)  # Will show: 15 10 30
    """
    pt = None
    if isinstance(reference, Point):
        pt = reference
    elif isinstance(reference, list):
        list_len = len(reference)
        for i in range(list_len):
            if isinstance(reference[-(i+1)], Point):
                pt = reference[-(i+1)]
                break
    if pt == None:
        raise Exception(f'The reference object must be a Point or a list containing at least one point')
    if None in [pt.x, pt.y, pt.z]:
        raise Exception(f'The reference point must have all of x, y, z attributes defined (x={pt.x}, y={pt.y}, z={pt.z})')
    new_pt = deepcopy(pt)
    new_pt.x, new_pt.y, new_pt.z = pt.x + x_offset, pt.y + y_offset, pt.z + z_offset
    return new_pt


def flatten(steps: list) -> list:
    """
    Flattens a nested list structure into a single-level list.

    This function takes a list that may contain nested lists and returns a new
    flattened list where all elements are at the top level. This is particularly
    useful for converting multi-dimensional designs into the 1D list structure
    required by FullControl for processing.

    Parameters:
        steps (list): The input list containing elements, some of which may be lists.

    Returns:
        list: A flattened 1D list.

    Example:
        >>> flatten([[1, 2], [3, 4], [5, 6]])
        [1, 2, 3, 4, 5, 6]
        
        >>> import fullcontrol as fc
        >>> points_a = [fc.Point(x=0, y=0, z=0), fc.Point(x=10, y=0, z=0)]
        >>> points_b = [fc.Point(x=10, y=10, z=0), fc.Point(x=0, y=10, z=0)]
        >>> design = [points_a, points_b]
        >>> flattened = flatten(design)  # Creates a 1D list with 4 points
    """
    return list(chain.from_iterable(step if isinstance(step, list) else [step]
                                    for step in steps))


def linspace(start: float, end: float, number_of_points: int) -> list:
    """
    Generate evenly spaced values from start to end.

    This function creates a list of evenly spaced values between start and end,
    similar to numpy's linspace function. It's useful for creating gradual
    transitions in designs.

    Args:
        start (float): The starting value of the range.
        end (float): The ending value of the range.
        number_of_points (int): The number of points to generate.

    Returns:
        list: A list of number_of_points floats, including the start and end values.
    
    Example:
        >>> linspace(0, 10, 5)
        [0.0, 2.5, 5.0, 7.5, 10.0]
    """
    return [start + float(x)/(number_of_points-1)*(end-start) for x in range(number_of_points)]


def first_point(steps: list, fully_defined: bool = True) -> Point:
    """
    Returns the first Point object from a list of steps.
    
    This function searches through a list of steps and returns the first
    Point object it finds. When fully_defined is True, it returns the first
    Point that has all x, y, and z coordinates defined (not None).
    
    Parameters:
        steps (list): A list of steps that may contain Point objects.
        fully_defined (bool): If True, return the first Point with all x, y, z values defined.
            If False, return the first Point regardless of whether all coordinates are defined.
    
    Returns:
        Point: The first Point in the list that meets the criteria.
    
    Raises:
        Exception: If no point is found in steps with all x, y, z values defined when fully_defined is True.
        Exception: If no point is found in steps when fully_defined is False.
    
    Example:
        >>> import fullcontrol as fc
        >>> steps = [fc.Extruder(on=True), fc.Point(x=0, y=0, z=0), fc.Point(x=10, y=10, z=10)]
        >>> point = first_point(steps)
        >>> print(point.x, point.y, point.z)  # Will show: 0 0 0
    """
    if isinstance(steps, list):
        for step in steps:
            if isinstance(step, Point):
                if fully_defined and any(val is None for val in (step.x, step.y, step.z)):
                    continue
                return step
    if fully_defined:
        raise Exception('No point found in steps with all of x y z defined')
    if not fully_defined:
        raise Exception('No point found in steps')
    
def last_point(steps: list, fully_defined: bool = True) -> Point:
    """
    Returns the last Point object from a list of steps.
    
    This function searches through a list of steps and returns the last
    Point object it finds. When fully_defined is True, it returns the last
    Point that has all x, y, and z coordinates defined (not None).
    
    Parameters:
        steps (list): A list of steps that may contain Point objects.
        fully_defined (bool): If True, return the last Point with all x, y, z values defined.
            If False, return the last Point regardless of whether all coordinates are defined.
    
    Returns:
        Point: The last Point in the list that meets the criteria.
    
    Raises:
        Exception: If no point is found in steps with all x, y, z values defined when fully_defined is True.
        Exception: If no point is found in steps when fully_defined is False.
    
    Example:
        >>> import fullcontrol as fc
        >>> steps = [fc.Point(x=0, y=0, z=0), fc.Point(x=10, y=10, z=10), fc.Extruder(on=False)]
        >>> point = last_point(steps)
        >>> print(point.x, point.y, point.z)  # Will show: 10 10 10
    """
    return first_point(list(reversed(steps)), fully_defined)


def export_design(steps: list, filename: str):
    """
    Export a design (list of steps) to a JSON file.

    This function serializes a FullControl design to a JSON file for later import.
    This allows saving designs for reuse or sharing with others.

    Parameters:
        steps (list): List of steps representing the design.
        filename (str): Name of the output JSON file (without .json extension).

    Returns:
        None
    
    Example:
        >>> import fullcontrol as fc
        >>> design = [fc.Point(x=0, y=0, z=0), fc.Point(x=10, y=10, z=10)]
        >>> export_design(design, "my_design")  # Creates my_design.json
    """
    import json
    with open(filename + '.json', 'w', encoding='utf-8') as f:
        json.dump(steps, f, ensure_ascii=False, indent=4, default=lambda x: {'type': type(x).__name__, 'data': x.__dict__})


def import_design(fc_module_handle, filename: str):
    """
    Import a previously exported design (list of steps).

    This function deserializes a design from a JSON file that was previously
    created with export_design. It reconstructs all the objects in the design
    using the provided FullControl module reference.

    Args:
        fc_module_handle: The fc module that was imported to create the design originally 
            (typically imported as 'fc' in most documentation examples).
        filename (str): The name of the file to import the design from (without the .json extension).

    Returns:
        list: A list of steps representing the imported design.
    
    Example:
        >>> import fullcontrol as fc
        >>> design = import_design(fc, "my_design")  # Loads from my_design.json
    """
    import json
    with open(filename + '.json') as f:
        data = json.load(f)
    steps = []
    for step in data:
        class_ = getattr(fc_module_handle, step['type'])
        step = class_.parse_obj(step['data'])
        steps.append(step)
    return steps
