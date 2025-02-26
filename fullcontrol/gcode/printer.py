from typing import Optional
from fullcontrol.common import Printer as BasePrinter

class Printer(BasePrinter):
    '''
    Extend generic class with gcode methods and attributes to convert the object to gcode

    Additional Attributes:
        command_list (Optional[dict]): A dictionary containing the printer's command list.
        new_command (Optional[dict]): A dictionary containing a new command to be added to the command list.
        speed_changed (Optional[bool]): A flag indicating whether the print speed or travel speed has changed.
    '''
    command_list: Optional[dict] = None
    new_command: Optional[dict] = None
    speed_changed: Optional[bool] = True  # Set to True by default to ensure speeds are always included initially

    def f_gcode(self, state):
        """
        Generate the G-code for the feedrate (F) based on the current state.

        Parameters:
        - state: The current state of the printer.

        Returns:
        - The G-code string for the feedrate (F) based on the current state.
        """
        current_speed = self.print_speed if state.extruder.on else self.travel_speed
        return f'F{current_speed}' + ' '

    def gcode(self, state):
        '''
        Process this instance in a list of steps supplied by the designer to generate and return a line of gcode.

        Args:
            state: The state object containing information about the printer's current state.

        Returns:
            A line of gcode generated based on the supplied steps.
        '''
        # Update all attributes of the tracking instance with the new instance (self)
        # and generate a G-code comment to document the change
        comment_lines = []
        
        # Handle print_speed
        if self.print_speed is not None:
            old_speed = state.printer.print_speed
            state.printer.print_speed = self.print_speed
            print(f"DEBUG Printer.gcode: Updated print_speed from {old_speed} to {self.print_speed}")
            comment_lines.append(f"; Set print_speed to {self.print_speed}")
            
        # Handle travel_speed
        if self.travel_speed is not None:
            old_speed = state.printer.travel_speed
            state.printer.travel_speed = self.travel_speed
            print(f"DEBUG Printer.gcode: Updated travel_speed from {old_speed} to {self.travel_speed}")
            comment_lines.append(f"; Set travel_speed to {self.travel_speed}")
            
        # Handle command list
        if self.new_command is not None:
            if state.printer.command_list is None:
                state.printer.command_list = {}
            state.printer.command_list = {**state.printer.command_list, **self.new_command}
            comment_lines.append("; Updated printer command list")
            
        # Return a comment line if any changes were made - this helps document the changes in the G-code output
        if comment_lines:
            return "\n".join(comment_lines)
        return None
