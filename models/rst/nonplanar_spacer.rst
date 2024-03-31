nonplanar spacer
================

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
    from math import cos, tau

.. code:: ipython3

    # printer/gcode parameters
    
    design_name = 'nonplanar_spacer'
    nozzle_temp = 210
    bed_temp = 40
    print_speed = 500
    fan_percent = 100
    printer_name='prusa_i3' # generic / ultimaker2plus / prusa_i3 / ender_3 / cr_10 / bambulab_x1 / toolchanger_T0

.. code:: ipython3

    # design parameters
    
    # main design parameters
    waves = 6
    # Waves - Number of waves around the circumference
    # default value: 6 ; guideline range: 1 to 10
    
    total_thickness = 4
    # Thickness (mm) - Total thickness of the spacer
    # default value: 4 ; guideline range: 0 to 10
    
    D1 = 8
    # Hole size (mm) - Diameter of inner hole
    # default value: 8 ; guideline range: 4 to 10
    
    
    # advanced parameters
    
    D_ratio = 3
    # Diameter ratio - Outer diameter is this value multiplied by hole size
    # default value: 3 ; guideline range: 1.5 to 5
    
    material_thickness = 0.4
    # Material thickness (mm) - Material thickness - recommended to be set equal to nozzle diameter - akin to conventional 'layer height' at the bottom of waves but may be more akin to conventional 'line width' at the top of waves
    # default value: 0.4 ; guideline range: 0.2 to 2
    
    EW_EH_ratio = 2
    # Extrudate aspect ratio - Ratio of extrusion width to extrusion height - a value of 2 is recommended for this structure
    # default value: 2 ; guideline range: 1 to 4
    
    overlap_percent = 20
    # Extrudate overlap % - Lateral overlap between adjacent extrudates - defined as a percentage of extrudate width - recommended value 10 to 20
    # default value: 20 ; guideline range: 0 to 40
    
    contraction_factor = 1.2
    # Wave contraction factor - Moves wave tips inwards... good for polymer squish. If set too low, structure may collapse. If set too high, the nozzle may scrape previous layer. Recommended value 1 to 1.2, maybe more for shallower structures.
    # default value: 1.2 ; guideline range: 0 to 2
    
    quantity = 1
    # Quantity - Number of parts to print
    # default value: 1 ; guideline range: 1 to 5
    

.. code:: ipython3

    # create design steps
    
    EH = material_thickness
    EW = EH*EW_EH_ratio
    D2 = D1*D_ratio 
    overlap = (overlap_percent/100) * EW 
    # increase in Z height of nozzle to get desired total_thickness:
    height = total_thickness - EH 
    R1, R2 = D1/2, D2/2
    rings = int((R2-R1)/(EW-overlap))
    segs_per_ring = (waves*2)*int(128/(waves*2)) # this means the segmented path always has a node at the exact min and max of waves
    
    centre = fc.Point(x=0, y=0, z=0)
    # set start point, and travel-line into centre of part:
    steps = [fc.move_polar(centre, centre, R2, (0.5+((waves+1)%2)/(2*waves))*tau), fc.Extruder(on=False), centre, fc.Extruder(on=True)]
    # add spiral purge line (if there is space):
    purge_spiral_passes = min(int((R1-EW)/EW)-1, 3)
    if purge_spiral_passes > 0: steps.extend(fc.spiralXY(centre, EW/2, R1-EW, 0, purge_spiral_passes, 200))
    
    # print part:
    for ring in range(rings):
      for seg in range(segs_per_ring+1):  # need one extra 'seg' to allow for the first segment having a start point as well as an end point
        angle_now = (seg/segs_per_ring)*tau
        z_now = height*(ring/(rings-1))*(0.5-0.5*cos(angle_now*waves))
        radius_now = R1 + EW/2 + ring*(EW-overlap)-(z_now*contraction_factor)
        centre.z = z_now
        steps.append(fc.polar_to_point(centre, radius_now, angle_now))
        
    # print multiple copies:
    if quantity > 1: steps = fc.move(steps, fc.Vector(x=R2*2 + 5), copy=True, copy_quantity=quantity)
    
    # offset the whole procedure. z dictates the gap between the nozzle and the bed for the first layer, assuming the model was designed with a first layer z-position of 0
    model_offset = fc.Vector(x=50, y=50, z=0.8*EH)
    steps = fc.move(steps, model_offset)

.. code:: ipython3

    # add annotations and plot
    
    annotations = []
    annotations.append(fc.PlotAnnotation(point=fc.midpoint(steps[0],steps[2]), label = "Initial approach set under a wave-crest to avoid defects"))
    annotations.append(fc.PlotAnnotation(point=steps[0], label = "Start"))
    annotations.append(fc.PlotAnnotation(point=steps[-1], label = "End"))
    annotations.append(fc.PlotAnnotation(point=fc.move(steps[2], fc.Vector(z=total_thickness*2)), label="A pointy nozzle is best"))
    if purge_spiral_passes>0: 
        annotations.append(fc.PlotAnnotation(point=steps[2], label="Spiral flow stabiliser"))
    if quantity > 1:
        annotations.append(fc.PlotAnnotation(point=fc.move(centre, fc.Vector(x=model_offset.x+(R2*2 + 5),
                           y=model_offset.y, z=model_offset.z)), label="Designed movement between parts and spiral-purge each time"))
        
    fc.transform(steps + annotations, 'plot', fc.PlotControls(color_type='print_sequence', initialization_data={'extrusion_width': EW, 'extrusion_height': EH}))

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
