fractional design engine demo (polar coordinates)
=================================================

*<<< check out other demo models*
`here <https://github.com/FullControlXYZ/fullcontrol/tree/master/models/README.md>`__
*>>>*

run all cells in this notebook, or press shift+enter to run each cell
sequentially

if you change one of the code cells, make sure you run it and all
subsequent cells again (in order)

*this document is a jupyter notebook - if they’re new to you, check out
how they work:*
`link <https://www.google.com/search?q=ipynb+tutorial>`__\ *,*
`link <https://jupyter.org/try-jupyter/retro/notebooks/?path=notebooks/Intro.ipynb>`__\ *,*
`link <https://colab.research.google.com/>`__

.. code:: ipython3

    import fullcontrol as fc
    from math import tau

.. code:: ipython3

    # printer/gcode parameters
    
    design_name = 'polar_design'
    nozzle_temp = 210
    bed_temp = 40
    print_speed = 1000
    fan_percent = 100
    printer_name='prusa_i3' # generic / ultimaker2plus / prusa_i3 / ender_3 / cr_10 / bambulab_x1 / toolchanger_T0

.. code:: ipython3

    # design parameters
    
    radius = 20
    # Nominal Radius (mm) - This radius is achieved when fractional radius is set to 1
    # default value: 20
    
    angle_fractions = [0, 0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9, 1]
    # Angle Fraction List (0-1) - List of fractional 'polar angles' for all points (angle increases anti-clockwise around a circle... 0 = positive x direction from centre, 0.25 = positive y direction, 1 is equivalent to 0) - google '2D polar angle' if unsure'
    # default value: [0,0.1,0.2,0.3,0.4,0.5,0.6,0.7,0.8,0.9,1]
    
    radial_fractions = [1, 0.5, 1, 0.5, 1, 0.5, 1, 0.5, 1, 0.5, 1]
    # Radii Fraction List (0-1) - List of fractional radii for all points (0 = centre of circle, 1 = nominal radius)
    # default value: [1,0.5,1,0.5,1,0.5,1,0.5,1,0.5,1]
    
    # Try a double-star (change all 0.5 radii to -0.5) or a coarse spiral (radii = [0.9, 0.91, 0.92, 0.93, 0.94, 0.95, 0.96, 0.97, 0.98, 0.99, 1])
    
    layers = 1
    # Layers - Number of layers to print - each layer is offset in Z by the extrusion height. Make sure layers finish at the same point they start
    # default value: 1
    
    centre_x, centre_y = 50, 50
    # XY centre - Centre of part in X and Y
    # default value: 50
    
    EW = 0.6
    # Extrusion Width (mm) - Width of printed lines - recommended value: 1.5x nozzle diameter
    # default value: 0.6
    
    EH = 0.2
    # Extrusion Height (mm) - Height of printed lines (i.e. layer thickness) - recommended value: 0.5x nozzle diameter
    # default value: 0.2
    
    travel_moves = [0]*len(angle_fractions)
    # Travel Instructions - A list of 0s and 1s (one for each point in the radii/angle lists) indicate whether to print to each point or travel to it. E.g. [0,0,0,0,0,0,0,0,0,0,1] prints all lines except the last one for the default model'
    # default value: [0]*len(angle_fractions)
    
    use_retraction = False
    # Use Retraction? - Set as True to use retraction commands (G10 and G11) before and after non-printing travel movements
    # default value: False
    
    initial_z = 0.8*EH # squash

.. code:: ipython3

    # generate the design (make sure you've run the above cells before running this cell)
    
    if len(angle_fractions) != len(radial_fractions) or len(angle_fractions) != len(travel_moves):
        raise Exception(f'the number of angles ({len(angle_fractions)}) / radii ({len(radial_fractions)}) / travel_moves-IDs ({len(travel_moves)}) in angle_fractions / radial_fractions / travel_moves must be the same')
    
    def travel_retract(existing_travel_state: int, new_travel_state: int, use_retraction: bool) -> list:
        if new_travel_state == existing_travel_state:
            return []
        elif new_travel_state == 0:
            return [fc.Extruder(on=True),  fc.PrinterCommand(id='unretract')] if use_retraction else [fc.Extruder(on=True)]
        elif new_travel_state == 1:
            return [fc.Extruder(on=False),  fc.PrinterCommand(id='retract')] if use_retraction else [fc.Extruder(on=False)]
        else:
            raise Exception(f'list of "travel_moves" must only include values of 0 or 1. current value: {new_travel_state}')
    
    centre = fc.Point(x=centre_x, y=centre_y, z=initial_z)
    
    steps = []
    existing_travel_state = 0
    for layer in range(int(layers)):
        for i in range(len(angle_fractions)):
            steps.extend(travel_retract(existing_travel_state, travel_moves[i], use_retraction))
            steps.append(fc.polar_to_point(centre, radius*radial_fractions[i], tau*angle_fractions[i]))
            existing_travel_state = travel_moves[i]
        centre.z += EH
    
    if fc.distance(steps[0], steps[-1]) > 0.001:
        steps.insert(1, fc.PlotAnnotation(label='start'))
        steps.append(fc.PlotAnnotation(label='end'))
    else:
        steps.append(fc.PlotAnnotation(label='start/end'))

.. code:: ipython3

    # preview the design
    
    # fc.transform(steps, 'plot', fc.PlotControls(style='line'))
    # hover the cursor over the lines in the plot to check xyz positions of the points in the design
    
    # uncomment the next line to create a plot with real heights/widths for extruded lines to preview the real 3D printed geometry
    fc.transform(steps, 'plot', fc.PlotControls(color_type='print_sequence', style='tube', initialization_data={'extrusion_width': EW, 'extrusion_height': EH}))
    
    # uncomment the next line to create a neat preview (click the top-left button in the plot for a .png file) - post and tag @FullControlXYZ :)
    # fc.transform(steps, 'plot', fc.PlotControls(neat_for_publishing=True, zoom=0.9,  initialization_data={'extrusion_width': EW, 'extrusion_height': EH}))
    

.. code:: ipython3

    # generate and save gcode
    
    gcode_controls = fc.GcodeControls(
        printer_name=printer_name,
        save_as=design_name,
        initialization_data={
            'primer': 'front_lines_then_y',
            'print_speed': print_speed,
            'nozzle_temp': nozzle_temp,
            'bed_temp': bed_temp,
            'fan_percent': fan_percent,
            'extrusion_width': EW,
            'extrusion_height': EH})
    gcode = fc.transform(steps, 'gcode', gcode_controls)
    

please tell us what you’re doing with FullControl!
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

-  tag FullControlXYZ on social media
   (`twitter <https://twitter.com/FullControlXYZ>`__,
   `instagram <https://www.instagram.com/fullcontrolxyz/>`__,
   `linkedin <https://www.linkedin.com/in/andrew-gleadall-068587119/>`__,
   `tiktok <https://www.tiktok.com/@fullcontrolxyz>`__)
-  email info@fullcontrol.xyz
-  post on the `subreddit <https://reddit.com/r/fullcontrol>`__
-  post in the `github discussions or issues
   tabs <https://github.com/FullControlXYZ/fullcontrol/issues>`__

in publications, please cite the original FullControl paper and the
github repo for the new python version:

-  Gleadall, A. (2021). FullControl GCode Designer: open-source software
   for unconstrained design in additive manufacturing. Additive
   Manufacturing, 46, 102109.
-  Gleadall, A. and Leas, D. (2023). FullControl [electronic resource:
   python source code]. available at:
   https://github.com/FullControlXYZ/fullcontrol
