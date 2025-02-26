from fullcontrol.gcode.printer import Printer
from typing import Optional, Dict, Any, Union
import json
import os

class GcodeControls:
    '''Class to control gcode generation.'''
    def __init__(self, printer_name: str = None, initialization_data: Dict[str, Any] = None, save_as: str = None, include_date: bool = True):
        self.printer_name = printer_name or 'generic'
        self.initialization_data = initialization_data or {}
        self.save_as = save_as
        self.include_date = include_date
        
        # Check for invalid printer name right away
        if printer_name and printer_name != 'generic':
            printer_path = os.path.join('printers', f'{printer_name}.json')
            if not os.path.exists(printer_path):
                raise ValueError(f"printer_name '{printer_name}' is invalid - printer configuration not found")
            
        # Never override user-provided values with defaults
        defaults = {
            'print_speed': 1000,
            'travel_speed': 2000,
            'extrusion_width': 0.4,
            'extrusion_height': 0.2,
            'relative_extrusion': True,
            'e_units': 'mm',
            'dia_feed': 1.75
        }
        
        # Only apply defaults for missing values
        for key, value in defaults.items():
            if key not in self.initialization_data:
                self.initialization_data[key] = value
            
        # Store custom G-code if provided
        self._custom_start_gcode = self.initialization_data.pop('start_gcode', None)
        self._custom_end_gcode = self.initialization_data.pop('end_gcode', None)

    def get_start_gcode(self) -> Optional[str]:
        """Get the start G-code sequence."""
        return self._custom_start_gcode

    def get_end_gcode(self) -> Optional[str]:
        """Get the end G-code sequence."""
        return self._custom_end_gcode

    def get_config(self, key: str, default: Any = None) -> Any:
        """Get a configuration value with fallback to default."""
        return self.initialization_data.get(key, default)

    def set_save_as(self, filename: str, include_date: bool = True):
        """Configure G-code file saving options."""
        self.save_as = filename
        self.include_date = include_date

    def initialize(self):
        """Post-initialization setup, mainly for handling late-bound settings."""
        # Re-check printer name
        if self.printer_name and self.printer_name != 'generic':
            printer_path = os.path.join('printers', f'{self.printer_name}.json')
            if not os.path.exists(printer_path):
                raise ValueError(f"Invalid printer_name '{self.printer_name}' - printer configuration not found")
        
        # Re-check default values after any post-init changes
        defaults = {
            'print_speed': 1000,
            'travel_speed': 2000,
            'extrusion_width': 0.4,
            'extrusion_height': 0.2,
            'relative_extrusion': True,
            'e_units': 'mm',
            'dia_feed': 1.75
        }
        
        # Only apply defaults for missing values
        for key, value in defaults.items():
            if key not in self.initialization_data:
                self.initialization_data[key] = value
