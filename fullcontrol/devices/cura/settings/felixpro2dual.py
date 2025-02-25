default_initial_settings = {
    "name": "Felix Pro 2 Dual",
    "manufacturer": "Felix",
    "start_gcode": """G90 ;absolute positioning
M82 ;set extruder to absolute mode
M107 ;start with the fan off
G28 X0 Y0 ;move X/Y to min endstops
G28 Z0 ;move Z to min endstops
G1 Z15.0 F9000 ;move the platform down 15mm

T0 ;Switch to the 1st extruder
G92 E0 ;zero the extruded length
G1 F200 E6 ;extrude 6 mm of feed stock
G92 E0 ;zero the extruded length again
;G1 F9000
M117 FPro2 printing...""",
    "end_gcode": """; Endcode FELIXprinters Pro series
; =================================	; Move extruder to park position
G91   					; Make coordinates relative
G1 Z2 F5000   				; Move z 2mm up
G90   					; Use absolute coordinates again		
G1 X220 Y243 F7800 			; Move bed and printhead to ergonomic position

; =================================	; Turn off heaters
T0					; Select left extruder
M104 T0 S0				; Turn off heater and continue				
G92 E0					; Reset extruder position
G1 E-8					; Retract filament 8mm
G1 E-5					; Push back filament 3mm
G92 E0					; Reset extruder position

T1					; Select right extruder
M104 T1 S0				; Turn off heater and continu
G92 E0					; Reset extruder position
G1 E-8					; Retract filament 8mm
G1 E-5					; Push back filament 3mm
G92 E0					; Reset extruder position
T0					; Select left extruder
M140 S0					; Turn off bed heater

; =================================	; Turn the rest off
M107    				; Turn off fan
M84					; Disable steppers
M117 Print Complete""",
    "bed_temp": 60,
    "nozzle_temp": 210,
    "material_flow_percent": 100,
    "print_speed": 80,
    "travel_speed": 120,
    "dia_feed": 2.85,
    "build_volume_x": 240,
    "build_volume_y": 225,
    "build_volume_z": 245,
}
