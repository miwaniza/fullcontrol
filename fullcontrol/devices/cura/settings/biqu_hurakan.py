default_initial_settings = {
    "name": "Biqu Hurakan",
    "manufacturer": "Biqu",
    "start_gcode": """;BIQU Hurakan start code. Much complex. Very wow. Klipper FTW.

START_PRINT BED_TEMP={data['bed_temp']} EXTRUDER_TEMP={data['nozzle_temp']}

; Note: This start/end code is designed to work
; with the stock cfg files provided  with the 
; BIQU Hurakan. If you alter the macros in the 
; cfg files then you may also need to alter this code.

; Another note: This profile will get you 
; part of the way to good prints.
; You still need to tweak settings for each 
; different filament that you use.
; Settings such as retraction distance/speed, 
; flow, pressure advance, bed/nozzle temperatures
; and others may need to be adjusted.
; Use https://teachingtechyt.github.io/calibration.html to calibrate.
; Also see https://www.youtube.com/watch?v=Ae2G7hl_pZc
; for some good tips.""",
    "end_gcode": """;BIQU Hurakan end code. More complex. Such wow. Klipper4Life.

END_PRINT""",
    "bed_temp": 60,
    "nozzle_temp": 210,
    "material_flow_percent": 100,
    "print_speed": 120,
    "travel_speed": 200,
    "dia_feed": 1.75,
    "build_volume_x": 235,
    "build_volume_y": 235,
    "build_volume_z": 270,
}
