nuts and bolts
==============

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
    import lab.fullcontrol as fclab

.. code:: ipython3

    # printer/gcode parameters
    
    design_name = 'nuts_and_bolts'
    nozzle_temp = 210
    bed_temp = 40
    print_speed = 1000
    fan_percent = 100
    printer_name='prusa_i3' # generic / ultimaker2plus / prusa_i3 / ender_3 / cr_10 / bambulab_x1 / toolchanger_T0

.. code:: ipython3

    # design parameters
    
    part_type = 'wing_bolt'  # wing_nut / wing_bolt / threaded_tube
    dia_major, dia_minor, pitch = 8.0, 6.75, 1.25     # M6: 6.0, 5.0, 1.0 / M8: 8.0, 6.75, 1.25 / M10: 10.0, 8.5, 1.5 / M12: 12.0, 10.25, 1.75
    bolt_or_tube_thread_length = 20 # ignored for wing_nut part_type
    wing_height = 0.75 * dia_major  # ignored for threaded_tube part_types
    clearance = 0.1 # this is the amount to undersize male threads or oversize female threads. if you 3D print both male and female threads, the clearance will effectively be doubled
    EH = 0.15 # extrusion height (layer height is set to this value)
    EW = 0.6 # extrusion width; recommended to be 1.5*nozzle_diameter

.. code:: ipython3

    # create design steps
    
    thread_type = 'female' if part_type == 'wing_nut' else 'male'
    wing_layers = int((wing_height)/EH)
    thread_layers = int((bolt_or_tube_thread_length)/EH) 
    if part_type == 'wing_nut': layers = wing_layers
    if part_type == 'wing_bolt': layers = wing_layers + thread_layers
    if part_type == 'threaded_tube': layers = thread_layers
    offset = EW/2+clearance
    rad_min = (dia_minor/2)-offset if thread_type == 'male' else (dia_minor/2)+offset
    rad_max = (dia_major/2)-offset if thread_type == 'male' else (dia_major/2)+offset
    segs = 64  # segments per layer
    a_shift = ((EH/segs)/pitch)*tau
    
    steps = []
    for i in range(layers):
        # print one layer of the thread 
        for j in range(segs):
            z_now = (i+(j/segs))*EH    
            a_max = (i*segs+j)*a_shift % tau
            a_now = (j/segs)*tau
            r_fraction_of_max = 1 - min(abs(a_now - a_max), abs(a_now - (a_max-tau)), abs(a_max - (a_now-tau)))/(tau/2)
            r_now = rad_min + r_fraction_of_max * (rad_max-rad_min)
            steps.append(fc.polar_to_point(fc.Point(x=0, y=0, z=z_now), r_now, a_now))
        # print one layer of the wings for wing-nut or wing-bolt part_types
        if part_type == 'wing_nut' or (part_type == 'wing_bolt' and i < wing_layers):
            centre_now = fc.Point(x=0, y=0, z=z_now)
            bezier_control_pts_1 = fc.rectangleXY(fc.polar_to_point(centre_now, rad_max+EW/4, 0), -(rad_max+EW/4)*2, dia_major*0.4, cw=True)[0:4]
            bezier_control_pts_1.insert(2, fc.Point(x=0, y=dia_major*2.25, z=z_now))
            steps.extend(fclab.bezierXYdiscrete(bezier_control_pts_1, 32))
            bezier_control_pts_2 = fc.move_polar(bezier_control_pts_1, centre_now, 0,tau/2)
            steps.extend(fclab.bezierXYdiscrete(bezier_control_pts_2, 32))
        # suggested design enhancement: 
            # repeat the above code for "print one layer of the thread" here and adjust r_now by -EW*0.8 to get two-wall print instead of single-wall (with 20% overlap between filament - hence the 0.8)
            # or instead of copying the code, an extra for loop around "for j in range(segs):" and reduce r_now -EW*0.8*loop_iteration to get as many walls as you like
            # or instead of solid reinforcement, design some kind of lattice inside
    
    model_offset = fc.Vector(x=50, y=50, z=0.333*EH) # the first layer gradually ramps up - it end at this offset + EH
    steps = fc.move(steps, model_offset)

.. code:: ipython3

    # preview the design
    
    # fc.transform(steps, 'plot', fc.PlotControls(style='line'))
    # hover the cursor over the lines in the plot to check xyz positions of the points in the design
    
    # uncomment the next line to create a plot with real heights/widths for extruded lines to preview the real 3D printed geometry
    fc.transform(steps, 'plot', fc.PlotControls(zoom=0.5, style='tube', initialization_data={'extrusion_width': EW, 'extrusion_height': EH}))
    
    # uncomment the next line to create a neat preview (click the top-left button in the plot for a .png file) - post and tag @FullControlXYZ :)
    # fc.transform(steps, 'plot', fc.PlotControls(neat_for_publishing=True, zoom=0.5,  initialization_data={'extrusion_width': EW, 'extrusion_height': EH}))
    

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
