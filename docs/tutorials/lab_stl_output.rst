lab stl output
==============

in addition to transforming a fullcontrol **design** into a ‘plot’
**result** or a ‘gcode’ **result**, it can also be transformed into a
‘3d_model’ **result** - that is a 3D model (e.g. stl file) of the
simulated as-printed geometry based on ``Point`` and
``ExtrusionGeometry`` objects in the **design**

this notebook briefly demonstrates how the 3D model can be generated

FullControl lab import
^^^^^^^^^^^^^^^^^^^^^^

.. code:: ipython3

    import fullcontrol as fc
    import lab.fullcontrol as fclab

create a **design**
^^^^^^^^^^^^^^^^^^^

.. code:: ipython3

    EW, EH = 0.8, 0.3 # extrusion width and height
    radius, layers = 10, 5
    design_name = 'test_design'
    steps = fc.helixZ(fc.Point(x=0, y=0, z=EH), radius, radius, 0, layers, EH, layers*32)

transform the design to a ‘plot’ **result** to preview it
'''''''''''''''''''''''''''''''''''''''''''''''''''''''''

.. code:: ipython3

    fc.transform(steps, 'plot', fc.PlotControls(style='tube', zoom=0.7,
                 initialization_data={'extrusion_width': EW, 'extrusion_height': EH}))

ModelControls adjust how a **design** is transformed into a ‘3d_model’ **result**
'''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''

**designs** are transformed into a ‘plot’ according to some default
settings which can be overwritten with a ``PlotControls`` object with
the following attributes (all demonstrated in this notebook):

-  ``stl_filename`` - string for filename (do not include ‘.stl’)
-  ``include_date`` - options: True/False (include dates/time-stamp in
   the stl filename)
-  ``tube_shape`` - options: ‘rectangle’ / ‘diamond’ / ‘hexagon’ /
   ‘octagon’ - adjusts cross sectional shape of extrudates in the stl
   file

   -  note this is a slightly different format than that used when
      generating 3D plots using ``tube-sides`` in a ``PlotControls``
      object

-  ``tube_type`` - options: ‘flow’/‘cylinders’ - adjust how the plot
   transitions from line to line

   -  see the ``PlotControls`` tutorial for more info about this
      parameter

-  ``stl_type`` - options: ‘ascii’/‘binary’ - stl file format
-  ``stls_combined`` - options: True/False - state whether **designs**
   containing multiple bodies are saved with all bodies in a single stl
   file - multiple bodies occur if the **design** includes
   non-extruding-travel moves between extruded regions
-  ``initialization_data`` - define initial width/height of 3D lines
   with dictionary: {‘extrusion_width’: value, ‘extrusion_height’:
   value} - these values are used until they are changed by an
   ``ExtrusionGeometry`` object in the **design**

.. code:: ipython3

    fclab.transform(steps, '3d_model', fclab.ModelControls(
        stl_filename=design_name, 
        include_date=False, 
        tube_shape='rectangle',
        tube_type= 'flow', 
        stl_type = 'ascii', 
        stls_combined = True, 
        initialization_data={'extrusion_width': EW, 'extrusion_height': EH}))

colab
^^^^^

if using google colab, the stl file can be downloaded from the file
browser on the left-hand side or with:

::

   from google.colab import files
   files.download(f'{design_name}.stl')

(assuming ``include_date`` is False)
