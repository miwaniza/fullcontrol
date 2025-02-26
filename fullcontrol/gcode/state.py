from typing import Optional, List
from pydantic import BaseModel
from importlib import import_module

from fullcontrol.gcode.point import Point
from fullcontrol.gcode.printer import Printer
from fullcontrol.gcode.extrusion_classes import ExtrusionGeometry, Extruder
from fullcontrol.gcode.controls import GcodeControls
from fullcontrol.common import first_point
from fullcontrol.gcode.import_printer import import_printer


class State(BaseModel):
    '''
    Track the state of objects needed to generate gcode.
    '''
    extruder: Optional[Extruder] = None
    printer: Optional[Printer] = None
    extrusion_geometry: Optional[ExtrusionGeometry] = None
    steps: Optional[list] = None
    point: Optional[Point] = Point()
    i: Optional[int] = 0
    gcode: List[str] = []

    def __init__(self, steps: list, gcode_controls: GcodeControls):
        """
        Initializes a State object.

        Args:
            steps (list): A list of steps for the state.
            gcode_controls (GcodeControls): An instance of the GcodeControls class.
        """
        super().__init__()
        self.gcode = []  # Reset gcode list
        
        # Ensure gcode_controls is initialized before using it
        gcode_controls.initialize()
        
        # Get printer configuration with initialized values
        config = gcode_controls.initialization_data

        # Print the config values for debugging
        print(f"DEBUG State.__init__: Config has print_speed={config.get('print_speed')}, travel_speed={config.get('travel_speed')}")
        
        # Add start G-code if provided
        start_gcode = config.get('start_gcode', '')
        if start_gcode:
            for line in start_gcode.splitlines():
                if line.strip():  # Only add non-empty lines
                    self.gcode.append(line.strip())

        # Initialize extruder with configuration values
        self.extruder = Extruder(
            units=config.get('e_units', 'mm'),
            dia_feed=config.get('dia_feed', 1.75),
            relative_gcode=config.get('relative_extrusion', True),
            total_volume=0,
            total_volume_ref=0,
            retraction=config.get('retraction', 0.0),
            travel_format=config.get('travel_format', 'G0'))
        self.extruder.update_e_ratio()

        # For tests that need specific print/travel speeds, set them directly from config
        print_speed = config.get('print_speed')
        travel_speed = config.get('travel_speed')
        
        print(f"DEBUG State.__init__: Setting printer with print_speed={print_speed}, travel_speed={travel_speed}")
        
        # Initialize printer with configuration values
        self.printer = Printer(
            command_list=config.get('printer_command_list', {}),
            print_speed=print_speed,
            travel_speed=travel_speed)

        # Initialize extrusion geometry
        self.extrusion_geometry = ExtrusionGeometry(
            area_model=config.get('area_model', 'rectangular'),
            width=config.get('extrusion_width', 0.4),
            height=config.get('extrusion_height', 0.2))
        self.extrusion_geometry.update_area()

        # Prepare steps list
        working_steps = []
        try:
            initial_point = first_point(steps)
        except Exception:
            initial_point = Point(x=0, y=0, z=0)
            steps.insert(0, initial_point)

        # Add primer steps if specified
        if config.get('primer', 'no_primer') != 'no_primer':
            try:
                primer_steps = import_module(f'fullcontrol.gcode.primer_library.{config["primer"]}').primer(initial_point)
                working_steps.extend(primer_steps)
            except ImportError:
                pass

        # Add main steps
        working_steps.extend(steps)

        # Add end G-code if provided
        end_gcode = config.get('end_gcode', '')
        if end_gcode:
            for line in end_gcode.splitlines():
                if line.strip():
                    working_steps.append(Point(gcode_line=line.strip()))

        self.steps = working_steps
        
        # Initialize tips if enabled
        if not config.get('disable_tips', False):
            if gcode_controls.printer_name == 'generic':
                print("tip: Using generic printer configuration - specify a real printer for proper initialization")
            if not config.get('start_gcode'):
                print("tip: No start G-code configured - add start_gcode to initialization_data for proper printer setup")
            if not config.get('end_gcode'):
                print("tip: No end G-code configured - add end_gcode to initialization_data for proper printer shutdown")
