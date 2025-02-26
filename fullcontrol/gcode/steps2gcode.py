import os
from fullcontrol.gcode import gcode
from fullcontrol.gcode.controls import GcodeControls
from fullcontrol.gcode.tips import tips
from datetime import datetime

def generate_gcode(steps: list, gcode_controls: GcodeControls, show_tips: bool = True) -> str:
    '''
    Generate a gcode string from a list of steps.

    Args:
        steps (list): A list of step objects.
        gcode_controls (GcodeControls): An instance of GcodeControls class.
        show_tips (bool): Whether to show usage tips.

    Returns:
        str: The generated gcode string.
    '''
    if show_tips:
        tips(gcode_controls)

    # Generate G-code using consolidated function
    result = gcode(steps, gcode_controls, show_tips=False)  # Tips already shown if needed

    # Save to file if configured
    if gcode_controls.save_as is not None:
        filename = gcode_controls.save_as
        if gcode_controls.include_date:
            filename += datetime.now().strftime("__%d-%m-%Y__%H-%M-%S")
        filename += ".gcode"
        with open(filename, 'w') as f:
            f.write(result)

    return result
