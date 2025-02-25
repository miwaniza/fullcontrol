from fullcontrol.gcode.controls import GcodeControls

def tips(controls: GcodeControls):
    tip_str = ''
    init_data = controls.initialization_data
    if 'extrusion_width' not in init_data and 'extrusion_height' not in init_data:
        tip_str += "\ntip: set initial `extrusion_width` and `extrusion_height` in the initialization_data to ensure the correct amount of material is extruded:\n   - `fc.transform(..., controls=fc.GcodeControls(initialization_data={'extrusion_width': EW, 'extrusion_height': EH}))`"
    elif 'extrusion_width' not in init_data:
        tip_str += "\ntip: set initial `extrusion_width` in the initialization_data:\n   - `fc.transform(..., controls=fc.GcodeControls(initialization_data={'extrusion_width': EW}))`"
    elif 'extrusion_height' not in init_data:
        tip_str += "\ntip: set initial `extrusion_height` in the initialization_data:\n   - `fc.transform(..., controls=fc.GcodeControls(initialization_data={'extrusion_height': EH}))`"
    
    if tip_str != '':
        print('fc.transform guidance tips are being written to screen if any potential issues are found - hide tips with fc.transform(..., show_tips=False)' + tip_str + '\n')
