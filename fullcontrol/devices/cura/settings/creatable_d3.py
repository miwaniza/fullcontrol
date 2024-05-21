default_initial_settings = {
    "name": "Creatable D3",
    "manufacturer": "Ateam Ventures Co. Ltd.",
    "start_gcode": "G21\nG90\nM82\nM106 S255\nG28\nG92 E0\nG1 Z100 F5000\nM190 S50\nM109 S200\nG1 X-135\nG1 Z0.3\nG92 E-32\nG1 E0 F1000\nG1 E50 F200\nG1 F1000\nG1 X-125\nG92 E0",
    "end_gcode": "M400\nG28\nM104 S0\nM140 S0\nM107\nG92 E0\nG1 E-32 F300\nM84\nG90",
    "bed_temp": 60,
    "nozzle_temp": 210,
    "material_flow_percent": 100,
    "print_speed": 60,
    "travel_speed": 120,
    "dia_feed": 2.85,
    "build_volume_x": 250,
    "build_volume_y": 250,
    "build_volume_z": 200,
}