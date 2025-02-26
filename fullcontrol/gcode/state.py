from typing import Optional, List, Union, TYPE_CHECKING

if TYPE_CHECKING:
    from fullcontrol.gcode.point import Point
    from fullcontrol.gcode.printer import Printer
    from fullcontrol.gcode.controls import GcodeControls
    from fullcontrol.gcode.extrusion_classes import ExtrusionGeometry, Extruder

class State:
    """Maintains state during G-code generation."""
    def __init__(self, steps: List[Union['Point', 'Printer']], controls: 'GcodeControls'):
        from fullcontrol.gcode.printer import Printer
        from fullcontrol.gcode.point import Point
        from fullcontrol.gcode.extrusion_classes import Extruder, ExtrusionGeometry
        
        self.steps = steps
        self.controls = controls
        self.gcode = []
        self.i = 0  # Initialize step counter
        
        # Initialize printer with default speeds from controls
        self.printer = Printer()
        self.printer.print_speed = controls.get_config('print_speed', 1000)  # Default 1000mm/min
        self.printer.travel_speed = controls.get_config('travel_speed', 2000)  # Default 2000mm/min
        self.printer.last_used_speed = None  # Track last used speed
        
        # Initialize extruder
        self.extruder = Extruder(
            relative_gcode=controls.get_config('relative_extrusion', True),
            units=controls.get_config('e_units', 'mm'),
            dia_feed=controls.get_config('dia_feed', 1.75)
        )
        
        # Initialize extrusion geometry
        self.extrusion_geometry = ExtrusionGeometry()
        if 'extrusion_width' in controls.initialization_data:
            self.extrusion_geometry.width = controls.initialization_data['extrusion_width']
        if 'extrusion_height' in controls.initialization_data:
            self.extrusion_geometry.height = controls.initialization_data['extrusion_height']
            
        # Initialize point
        self.point = Point(x=0, y=0, z=0)  # Start at origin
        
        # Initialize with start G-code if provided
        if controls.get_start_gcode():
            self.gcode.extend(line.strip() for line in controls.get_start_gcode().splitlines() if line.strip())
        
    def finalize(self):
        """Add end G-code if provided."""
        if self.controls.get_end_gcode():
            self.gcode.extend(line.strip() for line in self.controls.get_end_gcode().splitlines() if line.strip())
