default_initial_settings = {
    "name": "Tronxy D01",
    "manufacturer": "Tronxy",
    "start_gcode": "; D01 Start Code\nG21\nG90\nM82\nM107 T0\nM140 S{data['bed_temp']}\nM104 S{data['nozzle_temp']} T0\nM190 S{data['bed_temp']}\nM109 S{data['nozzle_temp']} T0\nG28\nG92 E0\nG1 Z2.0 F3000 ; Move Z Axis up little to preventscratching of Heat Bed\nG1 X1 Y20 Z0.3 F3600.0 ; Move to start position\nG1 X1 Y200.0 Z0.3 F1500.0 E25 ; Draw the first line\nG1 X1.6 Y200.0 Z0.3 F3600.0 ; Move to side a little\nG1 X1.6 Y20 Z0.3 F1500.0 E50 ; Draw the second line\nG92 E0 ; Reset Extruder\nG1 Z2.0 F3000 ; Move Z Axis up little to prevent scratching of Heat Bed\nG1 X5 Y20 Z0.3 F3600.0 ; Move over to prevent blob squish",
    "end_gcode": "M83 ; Set extrder to Relative\nG1 E-5 F3000 ; Retract 5mm of filament at 50mm/s\nG90 ; Set all axis to Absolute \nG1 X0 Y{data['build_volume_y']} ; Park print head\nG1 Z10 ; Move up 10mm\nM106 S0 ; Set fan speed to 0\nM104 S0 ; Set bed temp to 0\nM140 S0 ; Set Nozzle temp to 0\nM84 ; Disable all stepper motors\n",
    "bed_temp": 60,
    "nozzle_temp": 210,
    "material_flow_percent": 95,
    "print_speed": 60.0,
    "travel_speed": 75.0,
    "dia_feed": 1.75,
    "build_volume_x": 220,
    "build_volume_y": 220,
    "build_volume_z": 220,
}