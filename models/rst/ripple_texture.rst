ripple texture demo
===================

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
    from math import cos, tau, sin
    from copy import deepcopy

.. code:: ipython3

    # printer/gcode parameters
    
    design_name = 'ripples'
    nozzle_temp = 210
    bed_temp = 40
    print_speed = 500
    fan_percent = 100
    printer_name='prusa_i3' # generic / ultimaker2plus / prusa_i3 / ender_3 / cr_10 / bambulab_x1 / toolchanger_T0

.. code:: ipython3

    # design parameters
    
    inner_rad= 15
    # Inner Radius (mm) - Radius of the inner circle - 'star tip' and 'bulge' parameters morph the geometry radially outwards from this value
    # default value: 15 ; guideline range: 10 to 30
    
    height = 40
    # Height (mm) - Height of the part
    # default value: 40 ; guideline range: 20 to 80
    
    skew_percent = 10
    # Twist (%) - How much does the structure twist over its height? 100% means one full rotation anti-clockwise
    # default value: 10 ; guideline range: -100 to 100
    
    star_tips = 4
    # Star Tips - The number of outward protrusions from a nominally circular geometry - to make a star-like shape
    # default value: 4 ; guideline range: 0 to 10
    
    tip_length = 5
    # Star Tip Length (mm) - How much does each 'star tip' protrude beyond the inner radius?
    # default value: 5 ; guideline range: -20 to 20
    
    bulge = 2
    # Bulge (mm) - The geometry bulges out by this amount half way up the structure
    # default value: 2 ; guideline range: -20 to 20
    
    nozzle_dia = 0.4
    # Nozzle Diameter (mm) - This is used to set a reasonable value for layer height and extrusion rate
    # default value: 0.4 ; guideline range: 0.3 to 1.2
    
    ripples_per_layer = 50
    # Ripples Per Layer - Number of in-out waves the nozzle performs for each layer. There is actually an extra half-ripple for each layer so that the ripples are offset for each alternating layer
    # default value: 50 ; guideline range: 20 to 100
    
    rip_depth = 1
    # Ripple Depth (mm) - How far the nozzle moves in and out radially for each 'ripple'
    # default value: 1 ; guideline range: 0 to 5
    
    shape_factor = 1.5
    # Start Tip Pointiness - This affects how pointy the 'star tips' are and can achieve very interesting geometries
    # default value: 1.5 ; guideline range: 0.25 to 5
    
    
    RippleSegs = 2 # 2 means the ripple is zig-zag. increase this value to create a smooth wave, but watch out since the generation time will increase
    first_layer_E_factor = 0.4 # set to be 1 to double extrusion by the end of the layer, 0.4 adds 40%, which seemed good for me
    centre_x, centre_y = 50, 50

.. code:: ipython3

    # generate the design (make sure you've run the above cells before running this cell)
    
    EW = nozzle_dia*2.5
    EH = nozzle_dia*0.6
    centre = fc.Point(x=0, y=0, z=0)
    centre_now = deepcopy(centre)
    layers = int(height/EH)
    layer_segs = (ripples_per_layer+0.5)*RippleSegs
    total_segs = layer_segs*layers
    
    # offset the whole procedure to a convenient position on the print bed. initial_z dictates the gap between the nozzle and the bed for the first layer, assuming the model was designed with a first layer z-position of 0
    initial_z = 0.8*EH 
    model_offset = fc.Vector(x=centre_x, y=centre_y, z=initial_z)
    
    steps = []
    steps.append(fc.Printer(print_speed=print_speed/2)) # halve print speed for the first layer
    for t in range(int(layers*layer_segs)):
        t_val = t/layer_segs # tval = 0 to layers
        a_now = t_val*tau*(1+(skew_percent/100)/layers)
        a_now -= tau/4 # make the print start from front middle (near primer line)
        # the next equation (r_now) looks more complicated than it is. basically radius is inner_rad + radial fluctuation due to ripples (1st line) + radial fluctuation due to the star shape (2nd line) + radial fluctuation due to the bulge (3rd line)
        r_now = inner_rad + rip_depth*(0.5+(0.5*cos((ripples_per_layer+0.5)*(t_val*tau))))**1 + \
            (tip_length*(0.5-0.5*cos(star_tips*(t_val*tau)))**shape_factor) + \
            (bulge*(sin((centre_now.z/height)*(0.5*tau))))
        centre_now.z = t_val*EH
        if t_val < 1: # 1st layer
            steps.append(fc.ExtrusionGeometry(height=EH+EH*t_val*first_layer_E_factor)) # ramp up extrusion during the first layer since vase mode means the nozzle moves away from the buildplate
        if t_val == 1: # other layers
            steps.append(fc.ExtrusionGeometry(height=EH)) # reduce to the correct height as soon as the nozzle passes the start point of the previous layer
            steps.append(fc.Printer(print_speed = print_speed)) # double print speed after the first layer. this is combined with an instantaneous reduction in extrusion height, meaning volumetric flow rate would remain constant for this transition if first_layer_E_factor=1
        steps.append(fc.polar_to_point(centre_now, r_now, a_now))
    steps = fc.move(steps, model_offset)
    annotation_pts = []
    annotation_labels = []

.. code:: ipython3

    # preview the design
    
    # fc.transform(steps, 'plot', fc.PlotControls(zoom=0.4, style='line'))
    # hover the cursor over the lines in the plot to check xyz positions of the points in the design
    
    # uncomment the next line to create a plot with real heights/widths for extruded lines to preview the real 3D printed geometry
    fc.transform(steps, 'plot', fc.PlotControls(zoom=0.4, style='tube', initialization_data={'extrusion_width': EW, 'extrusion_height': EH}))
    
    # uncomment the next line to create a neat preview (click the top-left button in the plot for a .png file) - post and tag @FullControlXYZ :)
    # fc.transform(steps, 'plot', fc.PlotControls(neat_for_publishing=True, zoom=0.4,  initialization_data={'extrusion_width': EW, 'extrusion_height': EH}))
    

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
