from typing import Optional
from fullcontrol.common import Point as BasePoint


class Point(BasePoint):
    """A point in 3D space with G-code generation capabilities."""
    gcode_line: Optional[str] = None
    e: Optional[float] = None

    def __init__(self, **data):
        super().__init__(**data)
        self.gcode_line = data.get('gcode_line', None)
        self.e = data.get('e', None)

    def XYZ_gcode(self, p) -> str:
        '''Generate XYZ gcode string to move from a point p to this point.'''
        s = ''
        if self.x != None and self.x != p.x:
            s += f'X{self.x:.3f}'.rstrip('0').rstrip('.') + ' '
        if self.y != None and self.y != p.y:
            s += f'Y{self.y:.3f}'.rstrip('0').rstrip('.') + ' '
        if self.z != None and self.z != p.z:
            s += f'Z{self.z:.3f}'.rstrip('0').rstrip('.') + ' '
        return s if s != '' else None

    def gcode(self, state):
        """Generate G-code for movement to this point."""
        if not state or not state.printer:
            return None
            
        # If explicit G-code line is provided, use it
        if self.gcode_line:
            return self.gcode_line
            
        # Check if this is an extrusion move
        is_extrusion_move = False
        if self.e is not None or (state.extruder and state.extruder.on):
            is_extrusion_move = True
        
        # Get extrusion amount from state if not explicitly set
        e_value = self.e
        if e_value is None and is_extrusion_move and state.point:
            dx = (self.x - state.point.x) if self.x is not None and state.point.x is not None else 0
            dy = (self.y - state.point.y) if self.y is not None and state.point.y is not None else 0
            dz = (self.z - state.point.z) if self.z is not None and state.point.z is not None else 0
            move_length = (dx*dx + dy*dy + dz*dz) ** 0.5
            if state.extrusion_geometry:
                e_value = move_length * state.extrusion_geometry.get_extrusion_per_mm()
        
        # Determine G-code command type and speed
        g_command = "G1" if is_extrusion_move else "G0"
        speed = state.printer.print_speed if is_extrusion_move else state.printer.travel_speed
        
        # Build coordinates string using XYZ_gcode for consistent formatting
        coords = []
        xyz = self.XYZ_gcode(state.point if state.point else Point())
        if xyz:
            coords.append(xyz.strip())
        
        # Add extrusion if this is an extrusion move
        if is_extrusion_move and e_value is not None:
            coords.append(f"E{e_value:.4f}")
            
        # Add feedrate if speed is set and has changed
        if speed is not None:
            coords.append(f"F{int(speed)}")
            
        if coords:
            return f"{g_command} {' '.join(coords)}".strip()
        return None
