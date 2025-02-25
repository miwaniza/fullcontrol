default_initial_settings = {
    "name": "Flsun Q5",
    "manufacturer": "Flsun",
    "start_gcode": """;FLAVOR:Marlin
M82 ;absolute extrusion mode
G21
G90
M82
M107 T0
G28
G92 E0
G0 E3 F200
G92 E0 ; reset extrusion distance
M106 S255 ; Enable cooling fan full speed
G1 X-98 Y0 Z0.4 F3000 ; move to arc start
G3 X0 Y-98 I98 Z0.4 E40 F400 ; lay arc stripe 90deg
G92 E0 ; reset extrusion distance
G4 P500 ; wait for 0.5 sec
G0 Z10 E-1 ; Lift 15mm and retract 1mm filament
G4 P2000 ; wait for 5 sec
G0 Z15
M107 ; Disable cooling fan
G1 X0 Y-85 Z4 E0 F3000 ; get off the bed""",
    "end_gcode": """M104 S0
M140 S0
G92 E1
G1 E-1 F300
G28 X0 Y0
M84
M82 ;absolute extrusion mode
M104 S0""",
    "bed_temp": 60,
    "nozzle_temp": 210,
    "material_flow_percent": 100,
    "print_speed": 60,
    "travel_speed": 120,
    "dia_feed": 2.85,
    "build_volume_x": 200,
    "build_volume_y": 200,
    "build_volume_z": 200,
}
