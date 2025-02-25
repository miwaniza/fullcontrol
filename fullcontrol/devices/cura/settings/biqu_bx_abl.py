default_initial_settings = {
    "name": "Biqu BX",
    "manufacturer": "Biqu",
    "start_gcode": """; BIQU BX Start G-code
; For information on how to tune this profile and get the
; most out of your BX visit: https://github.com/looxonline/Marlin
; For the official github site visit: https://github.com/bigtreetech/BIQU-BX

M117 Initial homing sequence.                         ; Home so that the probe is positioned to heat
G28

M117 Probe heating position
G0 X65 Y5 Z1                                                   ; Move the probe to the heating position.

M117 Getting the heaters up to temp!
M104 S140                                                          ; Set Extruder temperature, no wait
M140 S60                                                            ; Set Heat Bed temperature
M190 S60                                                            ; Wait for Heat Bed temperature

M117 Waiting for probe to warm!                        ; Wait another 90s for the probe to absorb heat.
G4 S90 

M117 Post warming re-home
G28                                                                      ; Home all axes again after warming

M117 Z-Dance of my people
G34

M117 ABL Probing
G29

M900 K0 L0 T0                                 ;Edit the K and L values if you have calibrated a k factor for your filament
M900 T0 S0

G1 Z2.0 F3000                                        ; Move Z Axis up little to prevent scratching of Heat Bed
G1 X4.1 Y10 Z0.3 F5000.0                      ; Move to start position

M117 Getting the extruder up to temp
M140 S{data['bed_temp']}      ; Set Heat Bed temperature
M104 S{data['nozzle_temp']}    ; Set Extruder temperature
M109 S{data['nozzle_temp']}    ; Wait for Extruder temperature
M190 S{data['bed_temp']}      ; Wait for Heat Bed temperature

G92 E0                                        ; Reset Extruder
M117 Purging
G1 X4.1 Y200.0 Z0.3 F1500.0 E15               ; Draw the first line
G1 X4.4 Y200.0 Z0.3 F5000.0                   ; Move to side a little
G1 X4.4 Y20 Z0.3 F1500.0 E30                  ; Draw the second line
G92 E0                                        ; Reset Extruder
M117 Lets make
G1 X8 Y20 Z0.3 F5000.0                        ; Move over to prevent blob squish""",
    "end_gcode": """                               ;BIQU Default End Gcode
G91                            ;Relative positioning
G1 E-2 F2700                   ;Retract a bit
G1 E-2 Z0.2 F2400              ;Retract a bit more and raise Z
G1 X5 Y5 F3000                 ;Wipe out
G1 Z10                         ;Raise Z by 10mm
G90                            ;Return to absolute positioning

G1 X0 Y{data['build_volume_y']}         ;TaDaaaa
M106 S0                        ;Turn-off fan
M104 S0                        ;Turn-off hotend
M140 S0                        ;Turn-off bed

M84 X Y E                      ;Disable all steppers but Z
""",
    "bed_temp": 60,
    "nozzle_temp": 210,
    "material_flow_percent": 100,
    "print_speed": 50,
    "travel_speed": 150.0,
    "dia_feed": 1.75,
    "build_volume_x": 250,
    "build_volume_y": 250,
    "build_volume_z": 250,
}
