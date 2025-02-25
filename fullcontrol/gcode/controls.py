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
            return {
                'start_gcode': '',
                'end_gcode': '',
                'print_speed': 8000,
                'travel_speed': 8000,
                'retraction': 0,
                'z_hop': 0,
                'relative_extrusion': True
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

