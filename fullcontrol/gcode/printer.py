from typing import Optional, Dict, Any
from fullcontrol.common import Printer as BasePrinter

class PrinterCommand:
    """Base class for printer commands that can be converted to G-code."""
    def __init__(self, command: Dict[str, Any] = None):
        self.command = command or {}
        
    def gcode(self, state) -> Optional[str]:
        """Convert the command to G-code."""
        return None

class Printer(BasePrinter):
    '''
    Extend generic class with gcode methods and attributes to convert the object to gcode.
    '''
    command_list: Optional[dict] = None
    new_command: Optional[dict] = None
    print_speed: Optional[float] = None
    travel_speed: Optional[float] = None
    last_used_speed: Optional[float] = None
    
    def update_speed(self, state) -> Optional[str]:
        """Update and track speed changes."""
        if not state:
            return None
            
        speed = None
        is_extrusion = state.extruder and state.extruder.on
        if is_extrusion:
            speed = self.print_speed
        else:
            speed = self.travel_speed
            
        # Only emit speed command if it has changed
        if speed is not None and speed != state.printer.last_used_speed:
            state.printer.last_used_speed = speed
            return f"G1 F{int(speed)} ; Set {'print' if is_extrusion else 'travel'} speed"
        return None
    
    def update_from(self, other):
        """Update this printer's attributes from another printer instance."""
        super().update_from(other)
        if other.print_speed is not None:
            self.print_speed = other.print_speed
            # Reset last_used_speed to force speed update
            self.last_used_speed = None
        if other.travel_speed is not None:
            self.travel_speed = other.travel_speed
            # Reset last_used_speed to force speed update
            self.last_used_speed = None
        if other.new_command is not None:
            self.new_command = other.new_command.copy() if other.new_command else None
        if other.command_list is not None:
            if self.command_list is None:
                self.command_list = {}
            self.command_list.update(other.command_list)
        
    def gcode(self, state) -> Optional[str]:
        """Generate G-code for printer settings changes."""
        if not state:
            return None
            
        commands = []
        
        # Process speed changes with actual G-code
        speed_cmd = self.update_speed(state)
        if speed_cmd:
            commands.append(speed_cmd)
            
        # Process custom commands
        if self.new_command:
            if state.printer.command_list is None:
                state.printer.command_list = {}
            state.printer.command_list.update(self.new_command)
            for cmd, value in self.new_command.items():
                if isinstance(value, str):
                    commands.append(value)
                else:
                    commands.append(f"; Custom command: {cmd}={value}")
                
        # Update state's printer settings
        state.printer.update_from(self)
            
        return '\n'.join(commands) if commands else None
