FullControl AnyAngle Phone Stand
--------------------------------

this model is a more detailed version of that available on the
`fullcontrol website <https://fullcontrol.xyz/#/models/4d0e78>`__

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
    from math import cos, sin, tau
    from copy import deepcopy

.. code:: ipython3

    # printer/gcode parameters
    
    design_name = 'anyangle_phone_stand'
    nozzle_temp = 210
    bed_temp = 40
    material_flow_percent = 100
    print_speed_percent = 100
    fan_percent = 100
    printer_name='prusa_i3' # generic / ultimaker2plus / prusa_i3 / ender_3 / cr_10 / bambulab_x1 / toolchanger_T0

.. code:: ipython3

    # design parameters
    
    phone_width = 75
    # Phone Width (mm) - Measure with the case on if using one
    # default value: 75 ; guideline range: 10 to 200
    
    phone_thickness = 9
    # Phone Thickness (mm) - Measure with the case on if using one
    # default value: 9 ; guideline range: 4 to 20
    
    height = 30
    # Stand Height (mm) -
    # default value: 30 ; guideline range: 20 to 40
    
    angles = 13
    # Stand Angles (mm) - The number of angles the stand can orient the phone in landscape mode
    # default value: 13 ; guideline range: 9 to 19
    
    clamping_tightness_percent = 50
    # Clamping Tightness (%) - Increse this parameter to reduce the size of the stand and increase clamping forces on the phone
    # default value: 50 ; guideline range: 0 to 100
    
    wave_size_percent = 100
    # Wave Size (%) - Control how much the wave shapes of the stand protrude
    # default value: 100 ; guideline range: 50 to 150
    
    angry = False
    # Angry Mode - Make the phone stand look angry. Phone slots are not added in angry mode - set Stand Angles = 11 to 15 for a snug fit between the final two angry spikes
    # default value: False

.. code:: ipython3

    target = 'visualize'  # 'visualize' or 'gcode'

.. code:: ipython3

    # generate the design (make sure you've run the above cells before running this cell)
    
    # 0.3 # try 0.6, 0.3 or 1, 0.5 (slow speeds down proportionally for bigger size)
    EW, EH = 0.8, 0.4
    
    if target == "visualize":
        EH = 3*EH
    layers = int(height/EH)
    overlap = EW*0.25  # overlap between extrusions when the waves touch tip to tip
    initial_print_speed = 500  # print speed for the first layer
    # number of layers (after the first layer) during which speed increases
    layers_for_speed_increase = 2
    # print speed increases to this gradually over layers 2 & 3 (if layers_for_speed_increase=2)
    main_print_speed = 2*initial_print_speed
    
    
    amp_in_out = 3.25  # 3 # mm # 2.5?
    amp_mid = 2.25  # 2 # mm # 2.5?
    if angles % 2 < 0.000001:
        print('use an odd number of angles\n'*20)
    
    # centre point for the medial axis of the part
    centre = fc.Point(x=0, y=0, z=0)
    # -1 because there are two extra half-angles protruding to the front of the phone (extra_period_outer_inner)
    freq = (angles-1)*2
    angle_offset_outer_inner, angle_offset_mid = tau/2, tau/4  # phase shift for wave
    # how much of an extra sin period to print past 90 degres
    extra_period_outer_inner = 0.5
    extra_angle_outer_inner = (tau/((angles-1)*2))*extra_period_outer_inner
    # this is how much narrower the part is in the middle layer compared to top/bottom
    mid_contraction_fraction = 0.5
    # 0.1 #options 0.05, 0.075, 0.125# fraction by which the model's arc-radius is reduced and arc-length extended, to clamp the phone
    all_contraction_fraction = 0.05
    
    amp_in_out = amp_in_out*wave_size_percent/100
    all_contraction_fraction = all_contraction_fraction*clamping_tightness_percent/100
    
    segs = angles*8  # 8#4#8#16 # segments per half-circle plus an angle
    outer_wave_shape_factor, mid_wave_shape_factor, inner_wave_shape_factor = 2, 1.75, 1.5
    # 8,8,8#4,4,4#1.5,1,1 # 2,2,2#5,5,5 #3,1,2 #1.5,1,1...(GOOD FOR 13 ANGLES:2,1.5,1.5)
    
    # 8#4#16#32 # segments for each of the semicircles at the ends of the part
    segs_semicircles = 16
    
    if angry:
      outer_wave_shape_factor, mid_wave_shape_factor, inner_wave_shape_factor = 8, 8, 8
      segs_semicircles = 2
    
    # remove 1 mm from measure phone thickness due to typical rounded edges
    phone_thickness -= 1
    # this factor naturally increases the side of the slot, so it must be reduced now to compensate
    phone_thickness = phone_thickness*(1-all_contraction_fraction)
    
    # next line is means the sides of the phone protrude to the depth of the first fluctating sine wave (in2) as opposed to the medial axis
    medial_rad = phone_width/2 + amp_mid + EW
    rad_in2 = medial_rad - ((EW-overlap)/2) - amp_mid - (EW-overlap)
    rad_in1 = medial_rad - ((EW-overlap)/2) - amp_mid
    rad_out1 = medial_rad + ((EW-overlap)/2) + amp_mid
    rad_out2 = medial_rad + ((EW-overlap)/2) + amp_mid + (EW-overlap)
    
    centre_semicircle_top2 = fc.polar_to_point(
        centre, medial_rad, tau/4 - extra_angle_outer_inner)
    centre_semicircle_top1 = fc.polar_to_point(
        centre, medial_rad, tau/4 - extra_angle_outer_inner)
    centre_semicircle_bottom2 = fc.polar_to_point(
        centre, medial_rad, 3*tau/4 + extra_angle_outer_inner)
    centre_semicircle_bottom1 = fc.polar_to_point(
        centre, medial_rad, 3*tau/4 + extra_angle_outer_inner)
    
    # in2 arc to top
    mydesign = fc.arcXY(centre, rad_in2, tau/2, -
                        (tau/4+extra_angle_outer_inner), int(segs/2))
    line_id_list = ['in2']*(int(segs/2)+1)
    # top big semicircle
    mydesign += fc.arcXY(centre_semicircle_top2, medial_rad-rad_in2+amp_in_out,
                         3*tau/4 - extra_angle_outer_inner, tau/2, segs_semicircles)
    line_id_list += ['semicircle_top2']*(segs_semicircles+1)
    # out2 arc
    mydesign += fc.arcXY(centre, rad_out2, tau/4-extra_angle_outer_inner,
                         tau/2+extra_angle_outer_inner*2, segs)
    line_id_list += ['out2']*(segs+1)
    # bottom big semicircle
    mydesign += fc.arcXY(centre_semicircle_bottom2, medial_rad-rad_in2 +
                         amp_in_out, 3*tau/4 + extra_angle_outer_inner, tau/2, segs_semicircles)
    line_id_list += ['semicircle_bottom2']*(segs_semicircles+1)
    # in2 arc to middle
    mydesign += fc.arcXY(centre, rad_in2, 3*tau/4+extra_angle_outer_inner, -
                         (tau/4+extra_angle_outer_inner), int(segs/2))
    line_id_list += ['in2']*(int(segs/2)+1)
    
    # in1 arc to top
    mydesign += fc.arcXY(centre, rad_in1, tau/2, -
                         (tau/4+extra_angle_outer_inner), int(segs/2))
    line_id_list += ['in1']*(int(segs/2)+1)
    # top semicircle 1
    mydesign += fc.arcXY(centre_semicircle_top1, medial_rad-rad_in1,
                         3*tau/4 - extra_angle_outer_inner, tau/2, segs_semicircles)
    line_id_list += ['semicircle_top1']*(segs_semicircles+1)
    # out1 arc
    mydesign += fc.arcXY(centre, rad_out1, tau/4-extra_angle_outer_inner,
                         tau/2+extra_angle_outer_inner*2, segs)
    line_id_list += ['out1']*(segs+1)
    # bottom semicircle 1
    mydesign += fc.arcXY(centre_semicircle_bottom1, medial_rad-rad_in1,
                         3*tau/4 + extra_angle_outer_inner, tau/2, segs_semicircles)
    line_id_list += ['semicircle_bottom1']*(segs_semicircles+1)
    # in1 arc to middle
    mydesign += fc.arcXY(centre, rad_in1, 3*tau/4+extra_angle_outer_inner, -
                         (tau/4+extra_angle_outer_inner), int(segs/2))
    line_id_list += ['in1']*(int(segs/2)+1)
    
    points_per_layer = len(mydesign)
    
    for i in range(len(mydesign)):
      # calculate parameters
      radius_offset = 0
      angle_now = fc.point_to_polar(mydesign[i], centre).angle
      if angle_now < -0.00001:
          angle_now += tau
      line_id = line_id_list[i]
      # calculate radial offset
      if line_id == 'out2':
        radius_offset = amp_in_out * \
            (0.5+0.5*cos(angle_now*freq-angle_offset_outer_inner))**outer_wave_shape_factor
      elif line_id == 'in2':
        radius_offset = -amp_in_out * \
            (0.5+0.5*cos(angle_now*freq-angle_offset_outer_inner))**inner_wave_shape_factor
      if mydesign[i].x < 0:  # don't add a wave for the last bit of the middle lines so they can have a semicircle join their ends
        if line_id == 'out1':
          radius_offset = -amp_mid * \
              (0.5+0.5*cos(angle_now*freq-angle_offset_outer_inner))**mid_wave_shape_factor
        elif line_id == 'in1':
          radius_offset = amp_mid * \
              (0.5+0.5*cos(angle_now*freq-angle_offset_outer_inner))**mid_wave_shape_factor
      else:  # do a double reduced-period reduced-amplitude wave for the last one on inner section to end it within the outer loop
        if line_id == 'out1':
          radius_offset = -amp_mid * \
              (0.5+0.5*cos(2*angle_now*freq-angle_offset_outer_inner))**mid_wave_shape_factor
        elif line_id == 'in1':
          radius_offset = amp_mid * \
              (0.5+0.5*cos(2*angle_now*freq-angle_offset_outer_inner))**mid_wave_shape_factor
      # offset path as required
      mydesign[i] = fc.move_polar(mydesign[i], centre, radius_offset, 0)
    
    # slots
    if not angry:  # slots do not work well in angry mode
        for i in range(len(mydesign)):
            if line_id_list[i] == 'in2' or line_id_list[i] == 'semicircle_top2' or line_id_list[i] == 'semicircle_bottom2':
                slot_half_width = phone_thickness/2
                slot_half_height = phone_width/2+EW/2
                if abs(mydesign[i].x) <= slot_half_width and abs(mydesign[i].y) <= slot_half_height:
                    direction = mydesign[i].y/abs(mydesign[i].y)  # 1 or -1
                    mydesign[i].y = direction * \
                        (slot_half_height-(EW-overlap))  # make slot
                    # at curvature to end of slots and make sure they protrude by amp_in_out regardless of the shape/frequency of the inner wave
                    mydesign[i].y -= direction*amp_in_out * \
                        (1-cos((tau/4)*mydesign[i].x/(slot_half_width+EW)))**5
                elif abs(mydesign[i].x) <= slot_half_width+EW and abs(mydesign[i].y) <= slot_half_height:
                    direction = mydesign[i].y/abs(mydesign[i].y)  # 1 or -1
                    # make long side to slot (in case slot end is in a shallow bit of the inner wave)
                    mydesign[i].y = direction * \
                        (slot_half_height-(EW-overlap)-amp_in_out)
    
    # vase mode up for the last half period
    ramp_points = int(segs/(2*(angles-1)))
    for i in range(ramp_points):
      mydesign[-ramp_points +
               i] = fc.move(mydesign[-ramp_points+i], fc.Vector(z=EH*(i/ramp_points)))
    
    # layers = 1
    mydesign_multilayer = fc.flatten(
        [fc.move(mydesign, fc.Vector(z=EH*i)) for i in range(layers)])
    
    # narrow the walls towards the middle of the Z height
    for i in range(len(mydesign_multilayer)):
      z_fraction = mydesign_multilayer[i].z / height
      radius_now = fc.point_to_polar(mydesign_multilayer[i], centre).radius
      radius_offset = mid_contraction_fraction * \
          (medial_rad - radius_now) * (0.5-0.5*cos(z_fraction*tau))**0.5
      mydesign_multilayer[i] = fc.move_polar(
          mydesign_multilayer[i], centre, radius_offset, 0)
    
    # squash the design a bit so the phone expands it slightly and is therefore gripped better - proportionally reduce radius and increase arc length
    mydesign_squashed = []
    for i in range(len(mydesign_multilayer)):
        polar_now = fc.point_to_polar(mydesign_multilayer[i], centre)
        # make sure it is 0 to tau, not -pi to +pi
        angle_now = (polar_now.angle+tau) % tau
        angle_shift = (angle_now - tau/2)*all_contraction_fraction
        rad_shift = -polar_now.radius*all_contraction_fraction
        mydesign_squashed.append(fc.move_polar(
            mydesign_multilayer[i], centre, deepcopy(rad_shift), deepcopy(angle_shift)))
    
    mydesign_multilayer = mydesign_squashed
    
    # rotate design into a nicer print orientation
    mydesign_multilayer = fc.move_polar(mydesign_multilayer, centre, 0, -3*tau/8)
    
    # add speed control
    speed_increments = 100
    for i in range(speed_increments+1):
      speed_fraction = i/speed_increments
      mydesign_multilayer.insert(int(points_per_layer+speed_fraction*(layers_for_speed_increase*points_per_layer)),
                                 fc.Printer(print_speed=initial_print_speed + speed_fraction*(main_print_speed-initial_print_speed)))
    
    # generate gcode
    path_offset_xy = medial_rad + amp_in_out + amp_mid + 20
    
    
    # offset the whole procedure. z dictates the gap between the nozzle and the bed for the first layer, assuming the model was designed with a first layer z-position of 0
    model_offset = fc.Vector(x=path_offset_xy, y=path_offset_xy, z=0.8*EH)
    
    steps = fc.move(mydesign_multilayer, model_offset)
    

.. code:: ipython3

    # preview the design or save to gcode
    
    if target == 'gcode':
        # add point at start of print for a nice lead-in line
        steps.insert(0, fc.Point(x=path_offset_xy-medial_rad, y=path_offset_xy-medial_rad, z=steps[0].z))
        gcode_controls = fc.GcodeControls(
            printer_name=printer_name,
            save_as=design_name,
            initialization_data={
                'primer': 'front_lines_then_y',
                'print_speed': initial_print_speed,
                'nozzle_temp': nozzle_temp,
                'bed_temp': bed_temp,
                'fan_percent': fan_percent,
                'extrusion_width': EW,
                'extrusion_height': EH})
        gcode = fc.transform(steps, 'gcode', gcode_controls)
    else:
        # add annotations and plot
        steps.append(fc.PlotAnnotation(point=fc.Point(x=path_offset_xy, y=path_offset_xy, z=0), label='Zero-travel printpath'))
        steps.append(fc.PlotAnnotation(point=fc.Point(x=0.8*path_offset_xy, y=0.8*path_offset_xy, z=0), label='Not all layers shown in this preview'))
        steps.append(fc.PlotAnnotation(point=fc.Point(x=0.6*path_offset_xy, y=0.6*path_offset_xy, z=0), label="Print as fast as you can melt polymer - try speed=200% at +20'C"))
        if angry: 
            steps.append(fc.PlotAnnotation(point=fc.Point(x=0.4*path_offset_xy, y=0.4*path_offset_xy, z=0), label="Phone slots not added in angry mode - set Stand Angles = 11 to 15 for a snug fit between final two angry spikes"))
        elif angles > 13:
            steps.append(fc.PlotAnnotation(point=fc.Point(x=0.4*path_offset_xy, y=0.4*path_offset_xy, z=0), label='Phone slots not added in angry mode - set Stand Angles = 11 to 15 for a snug fit between final two angry spikes'))
        fc.transform(steps, 'plot', fc.PlotControls(style='line'))

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
