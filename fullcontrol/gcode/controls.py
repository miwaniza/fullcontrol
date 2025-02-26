from typing import Optional, Dict, Any
from pydantic import BaseModel, field_validator, model_validator
from importlib import import_module


class GcodeControls(BaseModel):
    """Control settings for G-code generation."""
    printer_name: str = "generic"
    initialization_data: Dict[str, Any] = {}
    save_as: Optional[str] = None
    include_date: bool = True

    @field_validator('printer_name')
    def validate_printer_name(cls, v: str) -> str:
        """Validate printer name exists and load its configuration."""
        if v != 'generic':
            try:
                printer_path = v.replace('/', '.').lower()
                import_module(f'fullcontrol.devices.community.{printer_path}')
            except ImportError:
                raise ValueError(f"Printer '{v}' is not supported. Make sure the printer configuration exists.")
        return v

    def get_printer_config(self) -> Dict[str, Any]:
        """Get the base printer configuration."""
        if self.printer_name == 'generic':
            # Return default generic config with basic settings
            return {
                'start_gcode': '',
                'end_gcode': '',
                # Default speeds, will be overwritten by initialization_data if provided
                'print_speed': 8000,
                'travel_speed': 8000,
                'retraction': 0,
                'z_hop': 0,
                'relative_extrusion': True,
                'extrusion_width': 0.4,
                'extrusion_height': 0.2,
                'e_units': 'mm',
                'dia_feed': 1.75,
                'manual_e_ratio': None,
                'printer_command_list': {},
                'area_model': 'rectangular',
                'primer': 'no_primer',
                'starting_procedure_steps': [],
                'ending_procedure_steps': []
            }
        
        try:
            printer_path = self.printer_name.replace('/', '.').lower()
            printer_module = import_module(f'fullcontrol.devices.community.{printer_path}')
            return getattr(printer_module, 'CONFIG', {})
        except (ImportError, AttributeError):
            return {}

    def get_config(self, key: str, default: Any = None) -> Any:
        """Get a configuration value, with initialization_data overriding printer defaults."""
        # Get base config first
        base_config = self.get_printer_config()
        # Override with initialization data
        config = {**base_config, **self.initialization_data}
        return config.get(key, default)

    def get_start_gcode(self) -> str:
        """Get the start G-code sequence."""
        return self.get_config('start_gcode', '')

    def get_end_gcode(self) -> str:
        """Get the end G-code sequence."""
        return self.get_config('end_gcode', '')

    def initialize(self) -> None:
        """Initialize printer configuration and show warnings if needed."""
        if self.printer_name == 'generic':
            print("warning: printer is not set - defaulting to 'generic', which does not initialize "
                  "the printer with proper start gcode\n   - use fc.transform(..., "
                  "controls=fc.GcodeControls(printer_name='generic') to disable this message or set "
                  "it to a real printer name\n")
        
        # Get the base printer configuration
        base_config = self.get_printer_config()
        
        # Handle initialization_data properly
        if not self.initialization_data:
            # If no initialization_data provided, use the base config
            self.initialization_data = base_config.copy()
        else:
            # Make a copy of the base config and update it with user-provided values
            # This ensures all base keys exist even if not explicitly provided by the user
            merged_config = base_config.copy()
            merged_config.update(self.initialization_data)
            self.initialization_data = merged_config
