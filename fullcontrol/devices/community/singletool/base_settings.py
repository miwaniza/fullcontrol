"""
Base settings for 3D printers in the FullControl community devices library.

This module defines default settings that serve as a baseline for all printer
configurations in the community singletool devices. These settings can be overridden
by printer-specific settings and user settings.

The default_initial_settings dictionary includes common settings for:
- Print and travel speeds
- Extrusion geometry and dimensions
- Temperature settings for various printer components
- Fan, flow and speed percentages
- Extrusion mode and units
- Standard printer commands for common operations
"""

default_initial_settings = {
    "print_speed": 1000,  # Print movement speed in mm/min
    "travel_speed": 8000,  # Travel (non-printing) movement speed in mm/min
    "area_model": "rectangle",  # Cross-section model for extrusion calculation
    "extrusion_width": 0.4,  # Width of extruded material in mm
    "extrusion_height": 0.2,  # Layer height in mm
    "nozzle_temp": 210,  # Hotend temperature in °C
    "bed_temp": 40,  # Build plate temperature in °C
    "enclosure_temp": 0,  # Enclosure temperature in °C (if supported)
    "tool_number": 0,  # Default tool number for multi-tool printers
    "fan_percent": 100,  # Part cooling fan speed as percentage
    "print_speed_percent": 100,  # Speed override percentage
    "material_flow_percent": 100,  # Extrusion multiplier as percentage
    "e_units": "mm",  # Extrusion units: "mm" for filament length or "mm3" for volume
    "relative_e": True,  # Whether to use relative extrusion mode
    "manual_e_ratio": None,  # Manual E ratio for custom extrusion control
    "dia_feed": 1.75,  # Filament diameter in mm
    "travel_format": "G0",  # G-code format for travel moves: "G0" or "G1_E0"
    "primer": "front_lines_then_y",  # Default primer routine to use
    "printer_command_list": {  # Common printer commands
        "home": "G28 ; home axes",
        "retract": "G10 ; retract",
        "unretract": "G11 ; unretract",
        "absolute_coords": "G90 ; absolute coordinates",
        "relative_coords": "G91 ; absolute coordinates",
        "units_mm": "G21 ; set units to millimeters"
    }
}
