from typing import List, Union, Optional, Sequence
from datetime import datetime
import os
import sys

def gcode(steps: Sequence[Union['Point', 'Printer', 'Fan', 'Hotend', 'Buildplate', 'ManualGcode', 'GcodeComment']], 
          controls: Optional['GcodeControls'] = None, 
          show_tips: bool = True) -> str:
    """Generate G-code from a list of steps."""
    from fullcontrol.gcode.state import State
    from fullcontrol.gcode.controls import GcodeControls
    from fullcontrol.gcode.point import Point
    from fullcontrol.gcode.printer import Printer
    from fullcontrol.gcode.manual_gcode import ManualGcode
    from fullcontrol.gcode.annotations import GcodeComment
    from fullcontrol.gcode.auxilliary_components import Fan, Hotend, Buildplate
    from fullcontrol.gcode.tips import tips

    if controls is None:
        controls = GcodeControls()

    if show_tips:
        # Display tips before any G-code generation
        tips(controls)

    # Create initial state with proper initialization
    state = State(steps, controls)
    
    # Force initial speed settings for first move
    state.printer.last_used_speed = None
    
    # Process each step
    for i, step in enumerate(steps):
        g_cmd = None
        
        # Handle Printer settings first
        if isinstance(step, Printer):
            state.printer.update_from(step)
            g_cmd = step.gcode(state)
        
        # Then handle extrusion state changes
        elif hasattr(step, 'gcode'):
            g_cmd = step.gcode(state)
            if isinstance(step, Point):
                state.point = step
        
        if g_cmd:
            if isinstance(g_cmd, str):
                state.gcode.append(g_cmd)
            elif isinstance(g_cmd, list):
                state.gcode.extend(g_cmd)
    
    # Add end G-code
    state.finalize()
    
    # Generate final G-code string
    result = '\n'.join(state.gcode)
    
    # Save to file if configured
    if controls.save_as:
        filename = controls.save_as
        if controls.include_date:
            filename += datetime.now().strftime("__%d-%m-%Y__%H-%M-%S")
        filename += ".gcode"
        # Create directories if they don't exist
        os.makedirs(os.path.dirname(filename) or '.', exist_ok=True)
        with open(filename, 'w') as f:
            f.write(result)
    
    return result

# Re-export commonly used classes
from fullcontrol.gcode.point import Point
from fullcontrol.gcode.printer import Printer, PrinterCommand
from fullcontrol.gcode.controls import GcodeControls
from fullcontrol.gcode.extrusion_classes import Extruder, ExtrusionGeometry, StationaryExtrusion
from fullcontrol.gcode.manual_gcode import ManualGcode
from fullcontrol.gcode.auxilliary_components import Fan, Hotend, Buildplate
from fullcontrol.gcode.annotations import GcodeComment
