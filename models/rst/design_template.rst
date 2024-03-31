FullControl design template
===========================

*<<< check out demo models*
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

.. code:: ipython3

    # printer/gcode parameters
    
    design_name = 'my_design'
    nozzle_temp = 210
    bed_temp = 40
    print_speed = 1000
    fan_percent = 100
    printer_name='prusa_i3' # generic / ultimaker2plus / prusa_i3 / ender_3 / cr_10 / bambulab_x1 / toolchanger_T0

.. code:: ipython3

    # design parameters
    
    EW = 0.8 # extrusion width
    EH = 0.3 # extrusion height (and layer height)
    initial_z = EH*0.6 # initial nozzle position is set to 0.6x the extrusion height to get a bit of 'squish' for good bed adhesion
    layers = 50

.. code:: ipython3

    # generate the design (make sure you've run the above cells before running this cell)
    
    steps = []
    for layer in range(layers):
      steps.append(fc.Point(x=50, y=50, z=initial_z+layer*EH))
      steps.append(fc.Point(x=100, y=50, z=initial_z+layer*EH))
      steps.append(fc.Point(x=100, y=100, z=initial_z+layer*EH))
      steps.append(fc.Point(x=50, y=100, z=initial_z+layer*EH))
      steps.append(fc.Point(x=50, y=50, z=initial_z+layer*EH))
      
    # instead of the above for-loop code, you can create the exact same design using built-in FullControl functions (uncomment the next two lines):
    # rectangle_steps = fc.rectangleXY(fc.Point(x=50, y=50, z=initial_z), 50, 50)
    # steps = fc.move(rectangle_steps, fc.Vector(z=EH), copy=True, copy_quantity=layers)

.. code:: ipython3

    # preview the design
    
    fc.transform(steps, 'plot', fc.PlotControls(style='line', zoom=0.7))
    # hover the cursor over the lines in the plot to check xyz positions of the points in the design
    
    # uncomment the next line to create a plot with real heights/widths for extruded lines to preview the real 3D printed geometry
    # fc.transform(steps, 'plot', fc.PlotControls(style='tube', zoom=0.7, initialization_data={'extrusion_width': EW, 'extrusion_height': EH}))
    
    # uncomment the next line to create a neat preview (click the top-left button in the plot for a .png file) - post and tag @FullControlXYZ :)
    # fc.transform(steps, 'plot', fc.PlotControls(neat_for_publishing=True, zoom=0.5, initialization_data={'extrusion_width': EW, 'extrusion_height': EH}))
    



.. raw:: html

    <div>                            <div id="48339c5f-ea6a-4bbb-bb70-bf77e901c3a3" class="plotly-graph-div" style="height:500px; width:800px;"></div>            <script type="text/javascript">                require(["plotly"], function(Plotly) {                    window.PLOTLYENV=window.PLOTLYENV || {};                                    if (document.getElementById("48339c5f-ea6a-4bbb-bb70-bf77e901c3a3")) {                    Plotly.newPlot(                        "48339c5f-ea6a-4bbb-bb70-bf77e901c3a3",                        [{"line":{"color":["rgb(0.00, 0.00, 255.00)","rgb(0.00, 0.00, 255.00)","rgb(0.00, 0.00, 255.00)","rgb(0.00, 0.00, 255.00)","rgb(0.00, 0.00, 255.00)","rgb(0.00, 5.10, 255.00)","rgb(0.00, 5.10, 255.00)","rgb(0.00, 5.10, 255.00)","rgb(0.00, 5.10, 255.00)","rgb(0.00, 5.10, 255.00)","rgb(0.00, 10.46, 255.00)","rgb(0.00, 10.46, 255.00)","rgb(0.00, 10.46, 255.00)","rgb(0.00, 10.46, 255.00)","rgb(0.00, 10.46, 255.00)","rgb(0.00, 15.55, 255.00)","rgb(0.00, 15.55, 255.00)","rgb(0.00, 15.55, 255.00)","rgb(0.00, 15.55, 255.00)","rgb(0.00, 15.55, 255.00)","rgb(0.00, 20.91, 255.00)","rgb(0.00, 20.91, 255.00)","rgb(0.00, 20.91, 255.00)","rgb(0.00, 20.91, 255.00)","rgb(0.00, 20.91, 255.00)","rgb(0.00, 26.01, 255.00)","rgb(0.00, 26.01, 255.00)","rgb(0.00, 26.01, 255.00)","rgb(0.00, 26.01, 255.00)","rgb(0.00, 26.01, 255.00)","rgb(0.00, 31.11, 255.00)","rgb(0.00, 31.11, 255.00)","rgb(0.00, 31.11, 255.00)","rgb(0.00, 31.11, 255.00)","rgb(0.00, 31.11, 255.00)","rgb(0.00, 36.46, 255.00)","rgb(0.00, 36.46, 255.00)","rgb(0.00, 36.46, 255.00)","rgb(0.00, 36.46, 255.00)","rgb(0.00, 36.46, 255.00)","rgb(0.00, 41.57, 255.00)","rgb(0.00, 41.57, 255.00)","rgb(0.00, 41.57, 255.00)","rgb(0.00, 41.57, 255.00)","rgb(0.00, 41.57, 255.00)","rgb(0.00, 46.92, 255.00)","rgb(0.00, 46.92, 255.00)","rgb(0.00, 46.92, 255.00)","rgb(0.00, 46.92, 255.00)","rgb(0.00, 46.92, 255.00)","rgb(0.00, 52.02, 255.00)","rgb(0.00, 52.02, 255.00)","rgb(0.00, 52.02, 255.00)","rgb(0.00, 52.02, 255.00)","rgb(0.00, 52.02, 255.00)","rgb(0.00, 57.12, 255.00)","rgb(0.00, 57.12, 255.00)","rgb(0.00, 57.12, 255.00)","rgb(0.00, 57.12, 255.00)","rgb(0.00, 57.12, 255.00)","rgb(0.00, 62.48, 255.00)","rgb(0.00, 62.48, 255.00)","rgb(0.00, 62.48, 255.00)","rgb(0.00, 62.48, 255.00)","rgb(0.00, 62.48, 255.00)","rgb(0.00, 67.58, 255.00)","rgb(0.00, 67.58, 255.00)","rgb(0.00, 67.58, 255.00)","rgb(0.00, 67.58, 255.00)","rgb(0.00, 67.58, 255.00)","rgb(0.00, 72.93, 255.00)","rgb(0.00, 72.93, 255.00)","rgb(0.00, 72.93, 255.00)","rgb(0.00, 72.93, 255.00)","rgb(0.00, 72.93, 255.00)","rgb(0.00, 78.03, 255.00)","rgb(0.00, 78.03, 255.00)","rgb(0.00, 78.03, 255.00)","rgb(0.00, 78.03, 255.00)","rgb(0.00, 78.03, 255.00)","rgb(0.00, 83.39, 255.00)","rgb(0.00, 83.39, 255.00)","rgb(0.00, 83.39, 255.00)","rgb(0.00, 83.39, 255.00)","rgb(0.00, 83.39, 255.00)","rgb(0.00, 88.48, 255.00)","rgb(0.00, 88.48, 255.00)","rgb(0.00, 88.48, 255.00)","rgb(0.00, 88.48, 255.00)","rgb(0.00, 88.48, 255.00)","rgb(0.00, 93.58, 255.00)","rgb(0.00, 93.58, 255.00)","rgb(0.00, 93.58, 255.00)","rgb(0.00, 93.58, 255.00)","rgb(0.00, 93.58, 255.00)","rgb(0.00, 98.94, 255.00)","rgb(0.00, 98.94, 255.00)","rgb(0.00, 98.94, 255.00)","rgb(0.00, 98.94, 255.00)","rgb(0.00, 98.94, 255.00)","rgb(0.00, 104.04, 255.00)","rgb(0.00, 104.04, 255.00)","rgb(0.00, 104.04, 255.00)","rgb(0.00, 104.04, 255.00)","rgb(0.00, 104.04, 255.00)","rgb(0.00, 109.39, 255.00)","rgb(0.00, 109.39, 255.00)","rgb(0.00, 109.39, 255.00)","rgb(0.00, 109.39, 255.00)","rgb(0.00, 109.39, 255.00)","rgb(0.00, 114.50, 255.00)","rgb(0.00, 114.50, 255.00)","rgb(0.00, 114.50, 255.00)","rgb(0.00, 114.50, 255.00)","rgb(0.00, 114.50, 255.00)","rgb(0.00, 119.59, 255.00)","rgb(0.00, 119.59, 255.00)","rgb(0.00, 119.59, 255.00)","rgb(0.00, 119.59, 255.00)","rgb(0.00, 119.59, 255.00)","rgb(0.00, 124.95, 255.00)","rgb(0.00, 124.95, 255.00)","rgb(0.00, 124.95, 255.00)","rgb(0.00, 124.95, 255.00)","rgb(0.00, 124.95, 255.00)","rgb(0.00, 130.05, 255.00)","rgb(0.00, 130.05, 255.00)","rgb(0.00, 130.05, 255.00)","rgb(0.00, 130.05, 255.00)","rgb(0.00, 130.05, 255.00)","rgb(0.00, 135.41, 255.00)","rgb(0.00, 135.41, 255.00)","rgb(0.00, 135.41, 255.00)","rgb(0.00, 135.41, 255.00)","rgb(0.00, 135.41, 255.00)","rgb(0.00, 140.51, 255.00)","rgb(0.00, 140.51, 255.00)","rgb(0.00, 140.51, 255.00)","rgb(0.00, 140.51, 255.00)","rgb(0.00, 140.51, 255.00)","rgb(0.00, 145.60, 255.00)","rgb(0.00, 145.60, 255.00)","rgb(0.00, 145.60, 255.00)","rgb(0.00, 145.60, 255.00)","rgb(0.00, 145.60, 255.00)","rgb(0.00, 150.96, 255.00)","rgb(0.00, 150.96, 255.00)","rgb(0.00, 150.96, 255.00)","rgb(0.00, 150.96, 255.00)","rgb(0.00, 150.96, 255.00)","rgb(0.00, 156.06, 255.00)","rgb(0.00, 156.06, 255.00)","rgb(0.00, 156.06, 255.00)","rgb(0.00, 156.06, 255.00)","rgb(0.00, 156.06, 255.00)","rgb(0.00, 161.41, 255.00)","rgb(0.00, 161.41, 255.00)","rgb(0.00, 161.41, 255.00)","rgb(0.00, 161.41, 255.00)","rgb(0.00, 161.41, 255.00)","rgb(0.00, 166.52, 255.00)","rgb(0.00, 166.52, 255.00)","rgb(0.00, 166.52, 255.00)","rgb(0.00, 166.52, 255.00)","rgb(0.00, 166.52, 255.00)","rgb(0.00, 171.62, 255.00)","rgb(0.00, 171.62, 255.00)","rgb(0.00, 171.62, 255.00)","rgb(0.00, 171.62, 255.00)","rgb(0.00, 171.62, 255.00)","rgb(0.00, 176.97, 255.00)","rgb(0.00, 176.97, 255.00)","rgb(0.00, 176.97, 255.00)","rgb(0.00, 176.97, 255.00)","rgb(0.00, 176.97, 255.00)","rgb(0.00, 182.07, 255.00)","rgb(0.00, 182.07, 255.00)","rgb(0.00, 182.07, 255.00)","rgb(0.00, 182.07, 255.00)","rgb(0.00, 182.07, 255.00)","rgb(0.00, 187.42, 255.00)","rgb(0.00, 187.42, 255.00)","rgb(0.00, 187.42, 255.00)","rgb(0.00, 187.42, 255.00)","rgb(0.00, 187.42, 255.00)","rgb(0.00, 192.53, 255.00)","rgb(0.00, 192.53, 255.00)","rgb(0.00, 192.53, 255.00)","rgb(0.00, 192.53, 255.00)","rgb(0.00, 192.53, 255.00)","rgb(0.00, 197.88, 255.00)","rgb(0.00, 197.88, 255.00)","rgb(0.00, 197.88, 255.00)","rgb(0.00, 197.88, 255.00)","rgb(0.00, 197.88, 255.00)","rgb(0.00, 202.98, 255.00)","rgb(0.00, 202.98, 255.00)","rgb(0.00, 202.98, 255.00)","rgb(0.00, 202.98, 255.00)","rgb(0.00, 202.98, 255.00)","rgb(0.00, 208.08, 255.00)","rgb(0.00, 208.08, 255.00)","rgb(0.00, 208.08, 255.00)","rgb(0.00, 208.08, 255.00)","rgb(0.00, 208.08, 255.00)","rgb(0.00, 213.44, 255.00)","rgb(0.00, 213.44, 255.00)","rgb(0.00, 213.44, 255.00)","rgb(0.00, 213.44, 255.00)","rgb(0.00, 213.44, 255.00)","rgb(0.00, 218.53, 255.00)","rgb(0.00, 218.53, 255.00)","rgb(0.00, 218.53, 255.00)","rgb(0.00, 218.53, 255.00)","rgb(0.00, 218.53, 255.00)","rgb(0.00, 223.89, 255.00)","rgb(0.00, 223.89, 255.00)","rgb(0.00, 223.89, 255.00)","rgb(0.00, 223.89, 255.00)","rgb(0.00, 223.89, 255.00)","rgb(0.00, 228.99, 255.00)","rgb(0.00, 228.99, 255.00)","rgb(0.00, 228.99, 255.00)","rgb(0.00, 228.99, 255.00)","rgb(0.00, 228.99, 255.00)","rgb(0.00, 234.09, 255.00)","rgb(0.00, 234.09, 255.00)","rgb(0.00, 234.09, 255.00)","rgb(0.00, 234.09, 255.00)","rgb(0.00, 234.09, 255.00)","rgb(0.00, 239.44, 255.00)","rgb(0.00, 239.44, 255.00)","rgb(0.00, 239.44, 255.00)","rgb(0.00, 239.44, 255.00)","rgb(0.00, 239.44, 255.00)","rgb(0.00, 244.54, 255.00)","rgb(0.00, 244.54, 255.00)","rgb(0.00, 244.54, 255.00)","rgb(0.00, 244.54, 255.00)","rgb(0.00, 244.54, 255.00)","rgb(0.00, 249.90, 255.00)","rgb(0.00, 249.90, 255.00)","rgb(0.00, 249.90, 255.00)","rgb(0.00, 249.90, 255.00)","rgb(0.00, 249.90, 255.00)","rgb(0.00, 255.00, 255.00)","rgb(0.00, 255.00, 255.00)","rgb(0.00, 255.00, 255.00)","rgb(0.00, 255.00, 255.00)","rgb(0.00, 255.00, 255.00)"],"width":4},"mode":"lines","showlegend":false,"x":[50.0,100.0,100.0,50.0,50.0,50.0,100.0,100.0,50.0,50.0,50.0,100.0,100.0,50.0,50.0,50.0,100.0,100.0,50.0,50.0,50.0,100.0,100.0,50.0,50.0,50.0,100.0,100.0,50.0,50.0,50.0,100.0,100.0,50.0,50.0,50.0,100.0,100.0,50.0,50.0,50.0,100.0,100.0,50.0,50.0,50.0,100.0,100.0,50.0,50.0,50.0,100.0,100.0,50.0,50.0,50.0,100.0,100.0,50.0,50.0,50.0,100.0,100.0,50.0,50.0,50.0,100.0,100.0,50.0,50.0,50.0,100.0,100.0,50.0,50.0,50.0,100.0,100.0,50.0,50.0,50.0,100.0,100.0,50.0,50.0,50.0,100.0,100.0,50.0,50.0,50.0,100.0,100.0,50.0,50.0,50.0,100.0,100.0,50.0,50.0,50.0,100.0,100.0,50.0,50.0,50.0,100.0,100.0,50.0,50.0,50.0,100.0,100.0,50.0,50.0,50.0,100.0,100.0,50.0,50.0,50.0,100.0,100.0,50.0,50.0,50.0,100.0,100.0,50.0,50.0,50.0,100.0,100.0,50.0,50.0,50.0,100.0,100.0,50.0,50.0,50.0,100.0,100.0,50.0,50.0,50.0,100.0,100.0,50.0,50.0,50.0,100.0,100.0,50.0,50.0,50.0,100.0,100.0,50.0,50.0,50.0,100.0,100.0,50.0,50.0,50.0,100.0,100.0,50.0,50.0,50.0,100.0,100.0,50.0,50.0,50.0,100.0,100.0,50.0,50.0,50.0,100.0,100.0,50.0,50.0,50.0,100.0,100.0,50.0,50.0,50.0,100.0,100.0,50.0,50.0,50.0,100.0,100.0,50.0,50.0,50.0,100.0,100.0,50.0,50.0,50.0,100.0,100.0,50.0,50.0,50.0,100.0,100.0,50.0,50.0,50.0,100.0,100.0,50.0,50.0,50.0,100.0,100.0,50.0,50.0,50.0,100.0,100.0,50.0,50.0,50.0,100.0,100.0,50.0,50.0,50.0,100.0,100.0,50.0,50.0,50.0,100.0,100.0,50.0,50.0,50.0,100.0,100.0,50.0,50.0],"y":[50.0,50.0,100.0,100.0,50.0,50.0,50.0,100.0,100.0,50.0,50.0,50.0,100.0,100.0,50.0,50.0,50.0,100.0,100.0,50.0,50.0,50.0,100.0,100.0,50.0,50.0,50.0,100.0,100.0,50.0,50.0,50.0,100.0,100.0,50.0,50.0,50.0,100.0,100.0,50.0,50.0,50.0,100.0,100.0,50.0,50.0,50.0,100.0,100.0,50.0,50.0,50.0,100.0,100.0,50.0,50.0,50.0,100.0,100.0,50.0,50.0,50.0,100.0,100.0,50.0,50.0,50.0,100.0,100.0,50.0,50.0,50.0,100.0,100.0,50.0,50.0,50.0,100.0,100.0,50.0,50.0,50.0,100.0,100.0,50.0,50.0,50.0,100.0,100.0,50.0,50.0,50.0,100.0,100.0,50.0,50.0,50.0,100.0,100.0,50.0,50.0,50.0,100.0,100.0,50.0,50.0,50.0,100.0,100.0,50.0,50.0,50.0,100.0,100.0,50.0,50.0,50.0,100.0,100.0,50.0,50.0,50.0,100.0,100.0,50.0,50.0,50.0,100.0,100.0,50.0,50.0,50.0,100.0,100.0,50.0,50.0,50.0,100.0,100.0,50.0,50.0,50.0,100.0,100.0,50.0,50.0,50.0,100.0,100.0,50.0,50.0,50.0,100.0,100.0,50.0,50.0,50.0,100.0,100.0,50.0,50.0,50.0,100.0,100.0,50.0,50.0,50.0,100.0,100.0,50.0,50.0,50.0,100.0,100.0,50.0,50.0,50.0,100.0,100.0,50.0,50.0,50.0,100.0,100.0,50.0,50.0,50.0,100.0,100.0,50.0,50.0,50.0,100.0,100.0,50.0,50.0,50.0,100.0,100.0,50.0,50.0,50.0,100.0,100.0,50.0,50.0,50.0,100.0,100.0,50.0,50.0,50.0,100.0,100.0,50.0,50.0,50.0,100.0,100.0,50.0,50.0,50.0,100.0,100.0,50.0,50.0,50.0,100.0,100.0,50.0,50.0,50.0,100.0,100.0,50.0,50.0,50.0,100.0,100.0,50.0,50.0,50.0,100.0,100.0,50.0,50.0,50.0,100.0,100.0,50.0],"z":[0.18,0.18,0.18,0.18,0.18,0.48,0.48,0.48,0.48,0.48,0.78,0.78,0.78,0.78,0.78,1.08,1.08,1.08,1.08,1.08,1.38,1.38,1.38,1.38,1.38,1.68,1.68,1.68,1.68,1.68,1.98,1.98,1.98,1.98,1.98,2.28,2.28,2.28,2.28,2.28,2.58,2.58,2.58,2.58,2.58,2.88,2.88,2.88,2.88,2.88,3.18,3.18,3.18,3.18,3.18,3.48,3.48,3.48,3.48,3.48,3.78,3.78,3.78,3.78,3.78,4.08,4.08,4.08,4.08,4.08,4.38,4.38,4.38,4.38,4.38,4.68,4.68,4.68,4.68,4.68,4.98,4.98,4.98,4.98,4.98,5.28,5.28,5.28,5.28,5.28,5.58,5.58,5.58,5.58,5.58,5.88,5.88,5.88,5.88,5.88,6.18,6.18,6.18,6.18,6.18,6.48,6.48,6.48,6.48,6.48,6.78,6.78,6.78,6.78,6.78,7.08,7.08,7.08,7.08,7.08,7.38,7.38,7.38,7.38,7.38,7.68,7.68,7.68,7.68,7.68,7.98,7.98,7.98,7.98,7.98,8.28,8.28,8.28,8.28,8.28,8.58,8.58,8.58,8.58,8.58,8.88,8.88,8.88,8.88,8.88,9.18,9.18,9.18,9.18,9.18,9.48,9.48,9.48,9.48,9.48,9.78,9.78,9.78,9.78,9.78,10.08,10.08,10.08,10.08,10.08,10.38,10.38,10.38,10.38,10.38,10.68,10.68,10.68,10.68,10.68,10.98,10.98,10.98,10.98,10.98,11.28,11.28,11.28,11.28,11.28,11.58,11.58,11.58,11.58,11.58,11.88,11.88,11.88,11.88,11.88,12.18,12.18,12.18,12.18,12.18,12.48,12.48,12.48,12.48,12.48,12.78,12.78,12.78,12.78,12.78,13.08,13.08,13.08,13.08,13.08,13.38,13.38,13.38,13.38,13.38,13.68,13.68,13.68,13.68,13.68,13.98,13.98,13.98,13.98,13.98,14.28,14.28,14.28,14.28,14.28,14.58,14.58,14.58,14.58,14.58,14.88,14.88,14.88,14.88,14.88],"type":"scatter3d"},{"marker":{"color":"red","size":2},"mode":"markers","showlegend":false,"x":[],"y":[],"z":[],"type":"scatter3d"}],                        {"template":{"data":{"barpolar":[{"marker":{"line":{"color":"rgb(17,17,17)","width":0.5},"pattern":{"fillmode":"overlay","size":10,"solidity":0.2}},"type":"barpolar"}],"bar":[{"error_x":{"color":"#f2f5fa"},"error_y":{"color":"#f2f5fa"},"marker":{"line":{"color":"rgb(17,17,17)","width":0.5},"pattern":{"fillmode":"overlay","size":10,"solidity":0.2}},"type":"bar"}],"carpet":[{"aaxis":{"endlinecolor":"#A2B1C6","gridcolor":"#506784","linecolor":"#506784","minorgridcolor":"#506784","startlinecolor":"#A2B1C6"},"baxis":{"endlinecolor":"#A2B1C6","gridcolor":"#506784","linecolor":"#506784","minorgridcolor":"#506784","startlinecolor":"#A2B1C6"},"type":"carpet"}],"choropleth":[{"colorbar":{"outlinewidth":0,"ticks":""},"type":"choropleth"}],"contourcarpet":[{"colorbar":{"outlinewidth":0,"ticks":""},"type":"contourcarpet"}],"contour":[{"colorbar":{"outlinewidth":0,"ticks":""},"colorscale":[[0.0,"#0d0887"],[0.1111111111111111,"#46039f"],[0.2222222222222222,"#7201a8"],[0.3333333333333333,"#9c179e"],[0.4444444444444444,"#bd3786"],[0.5555555555555556,"#d8576b"],[0.6666666666666666,"#ed7953"],[0.7777777777777778,"#fb9f3a"],[0.8888888888888888,"#fdca26"],[1.0,"#f0f921"]],"type":"contour"}],"heatmapgl":[{"colorbar":{"outlinewidth":0,"ticks":""},"colorscale":[[0.0,"#0d0887"],[0.1111111111111111,"#46039f"],[0.2222222222222222,"#7201a8"],[0.3333333333333333,"#9c179e"],[0.4444444444444444,"#bd3786"],[0.5555555555555556,"#d8576b"],[0.6666666666666666,"#ed7953"],[0.7777777777777778,"#fb9f3a"],[0.8888888888888888,"#fdca26"],[1.0,"#f0f921"]],"type":"heatmapgl"}],"heatmap":[{"colorbar":{"outlinewidth":0,"ticks":""},"colorscale":[[0.0,"#0d0887"],[0.1111111111111111,"#46039f"],[0.2222222222222222,"#7201a8"],[0.3333333333333333,"#9c179e"],[0.4444444444444444,"#bd3786"],[0.5555555555555556,"#d8576b"],[0.6666666666666666,"#ed7953"],[0.7777777777777778,"#fb9f3a"],[0.8888888888888888,"#fdca26"],[1.0,"#f0f921"]],"type":"heatmap"}],"histogram2dcontour":[{"colorbar":{"outlinewidth":0,"ticks":""},"colorscale":[[0.0,"#0d0887"],[0.1111111111111111,"#46039f"],[0.2222222222222222,"#7201a8"],[0.3333333333333333,"#9c179e"],[0.4444444444444444,"#bd3786"],[0.5555555555555556,"#d8576b"],[0.6666666666666666,"#ed7953"],[0.7777777777777778,"#fb9f3a"],[0.8888888888888888,"#fdca26"],[1.0,"#f0f921"]],"type":"histogram2dcontour"}],"histogram2d":[{"colorbar":{"outlinewidth":0,"ticks":""},"colorscale":[[0.0,"#0d0887"],[0.1111111111111111,"#46039f"],[0.2222222222222222,"#7201a8"],[0.3333333333333333,"#9c179e"],[0.4444444444444444,"#bd3786"],[0.5555555555555556,"#d8576b"],[0.6666666666666666,"#ed7953"],[0.7777777777777778,"#fb9f3a"],[0.8888888888888888,"#fdca26"],[1.0,"#f0f921"]],"type":"histogram2d"}],"histogram":[{"marker":{"pattern":{"fillmode":"overlay","size":10,"solidity":0.2}},"type":"histogram"}],"mesh3d":[{"colorbar":{"outlinewidth":0,"ticks":""},"type":"mesh3d"}],"parcoords":[{"line":{"colorbar":{"outlinewidth":0,"ticks":""}},"type":"parcoords"}],"pie":[{"automargin":true,"type":"pie"}],"scatter3d":[{"line":{"colorbar":{"outlinewidth":0,"ticks":""}},"marker":{"colorbar":{"outlinewidth":0,"ticks":""}},"type":"scatter3d"}],"scattercarpet":[{"marker":{"colorbar":{"outlinewidth":0,"ticks":""}},"type":"scattercarpet"}],"scattergeo":[{"marker":{"colorbar":{"outlinewidth":0,"ticks":""}},"type":"scattergeo"}],"scattergl":[{"marker":{"line":{"color":"#283442"}},"type":"scattergl"}],"scattermapbox":[{"marker":{"colorbar":{"outlinewidth":0,"ticks":""}},"type":"scattermapbox"}],"scatterpolargl":[{"marker":{"colorbar":{"outlinewidth":0,"ticks":""}},"type":"scatterpolargl"}],"scatterpolar":[{"marker":{"colorbar":{"outlinewidth":0,"ticks":""}},"type":"scatterpolar"}],"scatter":[{"marker":{"line":{"color":"#283442"}},"type":"scatter"}],"scatterternary":[{"marker":{"colorbar":{"outlinewidth":0,"ticks":""}},"type":"scatterternary"}],"surface":[{"colorbar":{"outlinewidth":0,"ticks":""},"colorscale":[[0.0,"#0d0887"],[0.1111111111111111,"#46039f"],[0.2222222222222222,"#7201a8"],[0.3333333333333333,"#9c179e"],[0.4444444444444444,"#bd3786"],[0.5555555555555556,"#d8576b"],[0.6666666666666666,"#ed7953"],[0.7777777777777778,"#fb9f3a"],[0.8888888888888888,"#fdca26"],[1.0,"#f0f921"]],"type":"surface"}],"table":[{"cells":{"fill":{"color":"#506784"},"line":{"color":"rgb(17,17,17)"}},"header":{"fill":{"color":"#2a3f5f"},"line":{"color":"rgb(17,17,17)"}},"type":"table"}]},"layout":{"annotationdefaults":{"arrowcolor":"#f2f5fa","arrowhead":0,"arrowwidth":1},"autotypenumbers":"strict","coloraxis":{"colorbar":{"outlinewidth":0,"ticks":""}},"colorscale":{"diverging":[[0,"#8e0152"],[0.1,"#c51b7d"],[0.2,"#de77ae"],[0.3,"#f1b6da"],[0.4,"#fde0ef"],[0.5,"#f7f7f7"],[0.6,"#e6f5d0"],[0.7,"#b8e186"],[0.8,"#7fbc41"],[0.9,"#4d9221"],[1,"#276419"]],"sequential":[[0.0,"#0d0887"],[0.1111111111111111,"#46039f"],[0.2222222222222222,"#7201a8"],[0.3333333333333333,"#9c179e"],[0.4444444444444444,"#bd3786"],[0.5555555555555556,"#d8576b"],[0.6666666666666666,"#ed7953"],[0.7777777777777778,"#fb9f3a"],[0.8888888888888888,"#fdca26"],[1.0,"#f0f921"]],"sequentialminus":[[0.0,"#0d0887"],[0.1111111111111111,"#46039f"],[0.2222222222222222,"#7201a8"],[0.3333333333333333,"#9c179e"],[0.4444444444444444,"#bd3786"],[0.5555555555555556,"#d8576b"],[0.6666666666666666,"#ed7953"],[0.7777777777777778,"#fb9f3a"],[0.8888888888888888,"#fdca26"],[1.0,"#f0f921"]]},"colorway":["#636efa","#EF553B","#00cc96","#ab63fa","#FFA15A","#19d3f3","#FF6692","#B6E880","#FF97FF","#FECB52"],"font":{"color":"#f2f5fa"},"geo":{"bgcolor":"rgb(17,17,17)","lakecolor":"rgb(17,17,17)","landcolor":"rgb(17,17,17)","showlakes":true,"showland":true,"subunitcolor":"#506784"},"hoverlabel":{"align":"left"},"hovermode":"closest","mapbox":{"style":"dark"},"paper_bgcolor":"rgb(17,17,17)","plot_bgcolor":"rgb(17,17,17)","polar":{"angularaxis":{"gridcolor":"#506784","linecolor":"#506784","ticks":""},"bgcolor":"rgb(17,17,17)","radialaxis":{"gridcolor":"#506784","linecolor":"#506784","ticks":""}},"scene":{"xaxis":{"backgroundcolor":"rgb(17,17,17)","gridcolor":"#506784","gridwidth":2,"linecolor":"#506784","showbackground":true,"ticks":"","zerolinecolor":"#C8D4E3"},"yaxis":{"backgroundcolor":"rgb(17,17,17)","gridcolor":"#506784","gridwidth":2,"linecolor":"#506784","showbackground":true,"ticks":"","zerolinecolor":"#C8D4E3"},"zaxis":{"backgroundcolor":"rgb(17,17,17)","gridcolor":"#506784","gridwidth":2,"linecolor":"#506784","showbackground":true,"ticks":"","zerolinecolor":"#C8D4E3"}},"shapedefaults":{"line":{"color":"#f2f5fa"}},"sliderdefaults":{"bgcolor":"#C8D4E3","bordercolor":"rgb(17,17,17)","borderwidth":1,"tickwidth":0},"ternary":{"aaxis":{"gridcolor":"#506784","linecolor":"#506784","ticks":""},"baxis":{"gridcolor":"#506784","linecolor":"#506784","ticks":""},"bgcolor":"rgb(17,17,17)","caxis":{"gridcolor":"#506784","linecolor":"#506784","ticks":""}},"title":{"x":0.05},"updatemenudefaults":{"bgcolor":"#506784","borderwidth":0},"xaxis":{"automargin":true,"gridcolor":"#283442","linecolor":"#506784","ticks":"","title":{"standoff":15},"zerolinecolor":"#283442","zerolinewidth":2},"yaxis":{"automargin":true,"gridcolor":"#283442","linecolor":"#506784","ticks":"","title":{"standoff":15},"zerolinecolor":"#283442","zerolinewidth":2}}},"scene":{"xaxis":{"backgroundcolor":"black","nticks":10,"range":[49.998999999999995,100.001]},"yaxis":{"backgroundcolor":"black","nticks":10,"range":[49.998999999999995,100.001]},"zaxis":{"backgroundcolor":"black","nticks":10,"range":[0,50.002]},"camera":{"eye":{"x":-0.7142857142857143,"y":-1.4285714285714286,"z":0.2142857142857143},"center":{"x":0,"y":0,"z":-0.5}},"aspectmode":"cube"},"margin":{"l":10,"r":10,"b":10,"t":10,"pad":4},"paper_bgcolor":"black","width":800,"height":500},                        {"responsive": true}                    ).then(function(){
    
    var gd = document.getElementById('48339c5f-ea6a-4bbb-bb70-bf77e901c3a3');
    var x = new MutationObserver(function (mutations, observer) {{
            var display = window.getComputedStyle(gd).display;
            if (!display || display === 'none') {{
                console.log([gd, 'removed!']);
                Plotly.purge(gd);
                observer.disconnect();
            }}
    }});
    
    // Listen for the removal of the full notebook cells
    var notebookContainer = gd.closest('#notebook-container');
    if (notebookContainer) {{
        x.observe(notebookContainer, {childList: true});
    }}
    
    // Listen for the clearing of the current output cell
    var outputEl = gd.closest('.output');
    if (outputEl) {{
        x.observe(outputEl, {childList: true});
    }}
    
                            })                };                });            </script>        </div>


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
