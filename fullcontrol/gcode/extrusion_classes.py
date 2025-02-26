from typing import Optional
from fullcontrol.common import ExtrusionGeometry as BaseExtrusionGeometry
from fullcontrol.common import Extruder as BaseExtruder
from fullcontrol.common import StationaryExtrusion as BaseStationaryExtrusion
from fullcontrol.gcode import Point
from math import pi, sqrt
from pydantic import root_validator


class ExtrusionGeometry(BaseExtrusionGeometry):
    'Extend generic class with gcode method to convert the object to gcode'
    def gcode(self, state):
        '''
        Process this instance in a list of steps supplied by the designer to generate and return a line of gcode.

        Args:
            state (State): The state object containing the extrusion geometry.

        Returns:
            str: The generated line of gcode.
        '''
        # update all attributes of the tracking instance with the new instance (self)
        state.extrusion_geometry.update_from(self)
        if self.width != None \
                or self.height != None \
                or self.diameter != None \
                or self.area_model != None:
            try:
                state.extrusion_geometry.update_area()
            except:
                pass  # in case not all parameters set yet


class StationaryExtrusion(BaseStationaryExtrusion):
    'Extend generic class with gcode method to convert the object to gcode'
    def gcode(self, state):
        'process this instance in a list of steps supplied by the designer to generate and return a line of gcode'
        state.printer.speed_changed = True
        return f'G1 F{self.speed} E{state.extruder.get_and_update_volume(self.volume)*state.extruder.volume_to_e:.6}'


class Extruder(BaseExtruder):
    '''
    Extend generic class with gcode methods and attributes to convert the object to gcode.

    This class is used to manage the state of the extruder and translate the design into GCode.

    Attributes:
        units (str, optional): The units for E in GCode. Options include 'mm' and 'mm3'. If not specified, a default unit is used.
        dia_feed (float, optional): The diameter of the feedstock filament.
        relative_gcode (bool, optional): A flag indicating whether to use relative GCode. If not specified, a default value is used.
        volume_to_e (float, optional): A factor to convert the volume of material into the value of 'E' in GCode. Calculated automatically.
        total_volume (float, optional): The current extrusion volume for the whole print. Calculated automatically.
        total_volume_ref (float, optional): The total extrusion volume reference value. This attribute is set to allow extrusion to be expressed relative to this point. For relative_gcode = True, it is reset for every line. Calculated automatically.
        travel_format (str, optional): The format for travel moves in the GCode. If not specified, a default format is used.
        retraction (float, optional): The retraction distance when the extruder is turned off.
    '''

    # gcode additions to generic Extruder class

    # GCode attributes, used to translate the design into gcode:
    # units for E in GCode ... options: 'mm' / 'mm3'
    units: Optional[str] = None
    dia_feed: Optional[float] = None  # diameter of the feedstock filament
    relative_gcode: Optional[bool] = None
    # attibutes not set by user ... calculated automatically:
    # factor to convert volume of material into the value of 'E' in gcode
    volume_to_e: Optional[float] = 1.0
    # current extrusion volume for whole print
    total_volume: Optional[float] = 0.0
    # total extrusion volume reference value - this attribute is set to allow extrusion to be expressed relative to this point (for relative_gcode = True, it is reset for every line)
    total_volume_ref: Optional[float] = 0.0
    travel_format: Optional[str] = None
    retraction: Optional[float] = None

    def get_and_update_volume(self, volume):
        '''Calculate the extrusion volume and update the total volume.

        Args:
            volume (float): The volume of material to be extruded.

        Returns:
            float: The extrusion volume relative to the total volume.
        '''
        self.total_volume += volume
        ret_val = self.total_volume - self.total_volume_ref
        if self.relative_gcode == True:
            self.total_volume_ref = self.total_volume
        # to make absolute extrusion work, check self.total_volume_ref and, if above a treshold value, reset extrusion (set extruder_now.e_total_vol_reference_for_gcode = extruder_now.e_total_vol; insert a G92 command next in the steplist)
        return ret_val

    def e_gcode(self, point1: Point, state) -> str:
        '''Generate the gcode for extrusion.

        Args:
            point1 (Point): The point at the end of the extrusion.
            state: The current state of the printer.

        Returns:
            str: The gcode component for extrusion.
        '''
        def distance_forgiving(point1: Point, point2: Point) -> float:
            '''Calculate the distance between two points. x, y or z components are ignored unless defined in both points

            Args:
                point1 (Point): The first point.
                point2 (Point): The second point.

            Returns:
                float: The distance between the two points.
            '''
            dist_x = 0 if point1.x == None or point2.x == None else point1.x - point2.x
            dist_y = 0 if point1.y == None or point2.y == None else point1.y - point2.y
            dist_z = 0 if point1.z == None or point2.z == None else point1.z - point2.z
            return sqrt(dist_x**2 + dist_y**2 + dist_z**2)
        
        # When a Point has an e value specified, use it directly
        if hasattr(point1, 'e') and point1.e is not None and point1.e > 0:
            print(f"DEBUG: Extruder.e_gcode: Point has e={point1.e}, setting extruder.on=True")
            return f"E{point1.e}"
        
        if self.on:
            length = distance_forgiving(point1, state.point)
            
            # Initialize extrusion values if not set
            if self.volume_to_e is None:
                self.volume_to_e = 1.0
            
            # Default area if not set
            area = 0.2  # Default area if not properly set
            
            # Try to get area from extrusion geometry
            if state.extrusion_geometry and hasattr(state.extrusion_geometry, 'area'):
                if state.extrusion_geometry.area is None:
                    try:
                        state.extrusion_geometry.update_area()
                    except Exception as e:
                        pass
                if state.extrusion_geometry.area is not None:
                    area = state.extrusion_geometry.area
            
            # Calculate and return E value
            e_value = self.get_and_update_volume(length * area) * self.volume_to_e
            return f'E{e_value:.6f}'.rstrip('0').rstrip('.')
        elif self.retraction and not self.on:
            # Handle retraction when extruder is turned off
            return f'E-{self.retraction}'
        else:
            if state.extruder.travel_format == 'G1_E0':
                # return 'E0' for relative extrusion or E(previous extrusion) for absolute extrusion
                return f'E{self.get_and_update_volume(0)*self.volume_to_e:.6f}'.rstrip('0').rstrip('.')
            else: 
                # return nothing if travel format does not require am E value
                return ''

    def update_e_ratio(self):
        '''Calculate the ratio for conversion from mm3 extrusion to units for E in gcode.'''
        try:  # try in case not all parameters set yet
            if self.units == "mm3":
                self.volume_to_e = 1
            elif self.units == "mm":
                self.volume_to_e = 1 / (pi*(self.dia_feed/2)**2)
        except:
            self.volume_to_e = 1.0  # Default if calculation fails

    def gcode(self, state):
        '''Process this instance in a list of steps supplied by the designer to generate and return a line of gcode.

        Args:
            state: The current state of the printer.

        Returns:
            str: The generated line of gcode.
        '''
        output = []
        # update all attributes of the tracking instance with the new instance (self)
        prev_on = state.extruder.on
        state.extruder.update_from(self)
        
        # Handle extruder state changes
        if self.on is not None:
            state.printer.speed_changed = True
            if not self.on and prev_on and self.retraction:
                # When turning extruder off with retraction enabled, do retraction
                output.append(f"G1 E-{self.retraction}")
            elif self.on and not prev_on and self.retraction:
                # When turning extruder on with retraction enabled, do recovery
                output.append(f"G1 E{self.retraction}")
                
        # Handle other extruder settings
        if self.units is not None or self.dia_feed is not None:
            state.extruder.update_e_ratio()
            
        if self.relative_gcode is not None:
            state.extruder.total_volume_ref = state.extruder.total_volume
            output.append("M83 ; relative extrusion" if state.extruder.relative_gcode 
                        else "M82 ; absolute extrusion\nG92 E0 ; reset extrusion position to zero")
        
        return "\n".join(output) if output else None
