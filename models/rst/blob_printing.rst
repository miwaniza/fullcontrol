blob printing
=============

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
    
    design_name = 'blobs'
    nozzle_temp = 210
    bed_temp = 40
    fan_percent = 100
    printer_name='prusa_i3' # generic / ultimaker2plus / prusa_i3 / ender_3 / cr_10 / bambulab_x1 / toolchanger_T0

.. code:: ipython3

    # design parameters
    
    tube_radius = 10  # overall radius of the tubular structure formed of lots of blobs
    blob_size = 1.6  # diameter of blobs (in XY plane)
    # percentage overlap between neighbouring blobs (in XY plane). this value is for the denser 'top/bottom' layers - for middle less-dense layers, the blobs are twice as far apart
    bloc_overlap_percent = 33
    layers = 10
    dense_layers = 2  # this is the number of layers at the top and bottom that have double the number of blobs. other layers have fewer blobs with a small gap in between
    extrusion_speed = 100  # speed of extrusion set in gcode for extrusion-only G1 commands. The units of this speed depend on your printer but are likely mm/min or mm3/min
    centre_x, centre_y = 50, 50

.. code:: ipython3

    # generate the design (make sure you've run the above cells before running this cell)
    
    
    blob_height = blob_size/2
    blob_spacing = blob_size*(1-bloc_overlap_percent/100)
    blob_vol = blob_height*blob_size**2
    initial_z = 0.95*blob_height
    
    
    def move_and_blob(steps: list, point: fc.Point, volume: float, extrusion_speed: float) -> list:
        steps.extend([point, fc.StationaryExtrusion(
            volume=volume, speed=extrusion_speed), fc.PlotAnnotation(label='')])
    
    
    blobs_per_layer = int(tau*tube_radius/blob_spacing)
    if blobs_per_layer % 2 != 0:
        # number of blobs increased by 1 to achieve an even number of blocks per layer
        blobs_per_layer += 1
    angle_between_blobs = tau/blobs_per_layer
    
    steps = []
    
    # add primer line to get flow going and get attachment to the print bed:
    steps.extend([fc.Extruder(on=True), fc.Point(x=tube_radius+20*blob_spacing, y=0, z=0), fc.Printer(print_speed=100),
                 fc.ExtrusionGeometry(width=blob_size, height=blob_height), fc.Point(x=tube_radius+10*blob_spacing), fc.Extruder(on=False)])
    
    # add primer of 10 blobs to get into steady-state conditions:
    primer_blob_pts = fc.segmented_line(fc.Point(x=tube_radius+10*blob_spacing, y=0, z=0), fc.Point(x=tube_radius, y=0, z=0), 10)
    for blob_pt in primer_blob_pts[1:-1]: move_and_blob(steps, blob_pt, blob_vol, extrusion_speed)
    
    # print all the blobs:
    for layer in range(layers):
        for blob in range(blobs_per_layer):
            if (layer < dense_layers or layer >= layers-dense_layers) or blob % 2 == 0:
                move_and_blob(steps, fc.polar_to_point(centre=fc.Point(x=0, y=0, z=layer *
                              blob_height), radius=tube_radius, angle=angle_between_blobs*blob), blob_vol, extrusion_speed)
        # move directly over the top of the first point so the nozzle moves directly up in Z to begin the second layer
        steps.append(fc.Point(x=0+tube_radius, y=0))
    
    # offset the whole procedure. z dictates the gap between the nozzle and the bed for the first layer, assuming the model was designed with a first layer z-position of 0
    model_offset = fc.Vector(x=centre_x, y=centre_y, z=initial_z)
    steps = fc.move(steps, model_offset)
    
    steps.append(fc.PlotAnnotation(point=fc.Point(x=centre_x, y=centre_y, z=blob_height*layers*2),
                 label=f'Nodes in this preview show where blobs are deposited, but do not represent the size of blobs'))
    steps.append(fc.PlotAnnotation(point=fc.Point(x=centre_x, y=centre_y, z=blob_height*layers*1.5),
                 label=f'For this blob volume ({blob_vol:.1f} mm3) a good blob extrusion speed may take about {blob_vol/4:.1f}-{blob_vol/2:.1f} seconds per blob'))

.. code:: ipython3

    # preview the design
    
    fc.transform(steps, 'plot', fc.PlotControls(style='line'))

.. code:: ipython3

    # generate and save gcode
    
    gcode_controls = fc.GcodeControls(
        printer_name=printer_name,
        save_as=design_name,
        initialization_data={
            'primer': 'travel',
            'nozzle_temp': nozzle_temp,
            'bed_temp': bed_temp,
            'fan_percent': fan_percent})
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
