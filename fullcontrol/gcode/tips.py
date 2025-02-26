from fullcontrol.gcode.controls import GcodeControls
import os

def tips(controls: GcodeControls):
    """Generate usage tips for G-code generation settings."""
    tip_str = []
    init_data = controls.initialization_data

    # Check printer configuration
    if controls.printer_name != 'generic':
        printer_config = os.path.join('printers', f'{controls.printer_name}.json')
        if not os.path.exists(printer_config):
            tip_str.append(f"Invalid printer_name '{controls.printer_name}' - printer configuration not found")

    # Check extrusion settings
    if not init_data.get('extrusion_width'):
        tip_str.append("extrusion_width not set - using default value of 0.4mm")
    if not init_data.get('extrusion_height'):
        tip_str.append("extrusion_height not set - using default value of 0.2mm")
    
    # Check speed settings
    if not init_data.get('print_speed'):
        tip_str.append("print_speed not set - using default value of 1000mm/min")
    if not init_data.get('travel_speed'):
        tip_str.append("travel_speed not set - using default value of 2000mm/min")

    # Check extrusion mode
    if 'relative_extrusion' not in init_data:
        tip_str.append("relative_extrusion not explicitly set - using default (relative mode)")

    if tip_str:
        # Print header only if there are tips to show
        print("G-code generation tips (hide with show_tips=False):")
        for tip in tip_str:
            print(f"  tip: {tip}")
        print()
