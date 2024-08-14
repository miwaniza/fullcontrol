import re
from math import tau
from copy import deepcopy
from openai import OpenAI

import fullcontrol as fc


class LLMCall:
    def __init__(self, prompt, input_file, output_file):
        self.client = OpenAI()
        self.fix = prompt
        self.input_file = 'functions_template.py'
        if input_file:
            self.input_file = input_file
        self.output_file = 'functions_generated.py'
        if output_file:
            self.output_file = output_file
        self.prompt = f"""
        {self.fix}
        Params passed to function: inner_radius,ripple_depth,ripples_per_layer,tip_length,star_tips,shape_factor,bulge,height,centre_now_z
        Sample:
        """

    def read_calculate_effects(self):
        with open(self.input_file, 'r') as file:
            lines = file.readlines()
        return "".join(lines)

    def generate_function(self):
        print("Generating function...")
        completion = self.client.chat.completions.create(
            model="gpt-4o",
            messages=[
                {"role": "system",
                 "content": "You are a Python coder, that returns only code."},
                {"role": "user", "content": f"Modify function, so {self.prompt}.\n\n {self.read_calculate_effects()}"}
            ]
        )
        generated_function = completion.choices[0].message.content
        print("Function generated!")
        generated_function = re.search(
            r"```python\n([\s\S]*)\n```", generated_function).group(1)
        with open(self.output_file, 'w') as file:
            file.write(generated_function)


class PrinterSettings:
    def __init__(self, name, nozzle_temp, bed_temp, print_speed, fan_percent):
        self.name = name
        self.nozzle_temp = nozzle_temp
        self.bed_temp = bed_temp
        self.print_speed = print_speed
        self.fan_percent = fan_percent


class DesignParameters:
    def __init__(self, inner_radius, height, skew_percent, star_tips, tip_length, bulge,
                 nozzle_diameter, ripples_per_layer, ripple_depth, shape_factor):
        self.inner_radius = inner_radius
        self.height = height
        self.skew_percent = skew_percent
        self.star_tips = star_tips
        self.tip_length = tip_length
        self.bulge = bulge
        self.nozzle_diameter = nozzle_diameter
        self.ripples_per_layer = ripples_per_layer
        self.ripple_depth = ripple_depth
        self.shape_factor = shape_factor


class PrintJob:
    def __init__(self, design_params, printer_settings, ripple_segs, first_layer_e_factor, centre_x, centre_y):
        self.design_params = design_params
        self.printer_settings = printer_settings
        self.ripple_segs = ripple_segs
        self.first_layer_e_factor = first_layer_e_factor
        self.centre_x = centre_x
        self.centre_y = centre_y

        self.ew = self.design_params.nozzle_diameter * 2.5
        self.eh = self.design_params.nozzle_diameter * 0.6
        self.centre = fc.Point(x=0, y=0, z=0)
        self.centre_now = deepcopy(self.centre)
        self.layers = int(self.design_params.height / self.eh)
        self.layer_segs = (self.design_params.ripples_per_layer + 0.5) * self.ripple_segs
        self.total_segs = self.layer_segs * self.layers
        self.initial_z = 0.8 * self.eh
        self.model_offset = fc.Vector(x=self.centre_x, y=self.centre_y, z=self.initial_z)

        self.steps = []

    def generate_steps(self):
        print('Generating steps...')
        self.steps.append(
            fc.Printer(print_speed=self.printer_settings.print_speed / 2))  # Halve print speed for the first layer
        print('Generating function...')
        llm = LLMCall(
            'Vase should be in shape of trefoil knot',
            'functions_template.py',  # template file to be modified
            'functions_generated.py'  # file to be generated from template using LLM and prompt
        )
        llm.generate_function()
        print('Function generated.')

        self.steps = [
            step
            for t in range(int(self.layers * self.layer_segs))
            for t_val in [t / self.layer_segs]
            for a_now in [t_val * tau * (1 + (self.design_params.skew_percent / 100) / self.layers) - tau / 4]
            for r_now in [
                self.step_generator(t_val)
            ]
            for _ in [setattr(self.centre_now, 'z', t_val * self.eh)]
            for step in (
                [fc.ExtrusionGeometry(height=self.eh + self.eh * t_val * self.first_layer_e_factor)] if t_val < 1 else
                ([fc.ExtrusionGeometry(height=self.eh),
                  fc.Printer(print_speed=self.printer_settings.print_speed)] if t_val == 1 else
                 []) + [fc.polar_to_point(self.centre_now, r_now, a_now)]
            )
        ]
        print('Steps generated.')

        self.steps = fc.move(self.steps, self.model_offset)

    def step_generator(self, t_val):
        params = {
            'inner_radius': self.design_params.inner_radius,
            'ripple_depth': self.design_params.ripple_depth,
            'ripples_per_layer': self.design_params.ripples_per_layer,
            'tip_length': self.design_params.tip_length,
            'star_tips': self.design_params.star_tips,
            'shape_factor': self.design_params.shape_factor,
            'bulge': self.design_params.bulge,
            'height': self.design_params.height,
            'centre_now_z': self.centre_now.z
        }
        print('Calculating effects...')
        from models.ripple_texture_ai.functions_generated import calculate_effects
        result = calculate_effects(params, t_val)
        print('Effects calculated.')
        return result

    def preview_design(self):
        fc.transform(self.steps, 'plot', fc.PlotControls(zoom=0.4, style='tube',
                                                         initialization_data={'extrusion_width': self.ew,
                                                                              'extrusion_height': self.eh}))

    def generate_gcode(self):
        gcode_controls = fc.GcodeControls(
            printer_name=self.printer_settings.name,
            save_as=DESIGN_NAME,
            initialization_data={
                'primer': 'front_lines_then_y',
                'print_speed': self.printer_settings.print_speed,
                'nozzle_temp': self.printer_settings.nozzle_temp,
                'bed_temp': self.printer_settings.bed_temp,
                'fan_percent': self.printer_settings.fan_percent,
                'extrusion_width': self.ew,
                'extrusion_height': self.eh
            })
        gcode = fc.transform(self.steps, 'gcode', gcode_controls)
        return gcode


DESIGN_NAME = 'ripples'

# Define printer settings
printer_settings = PrinterSettings(
    name='prusa_i3',
    nozzle_temp=210,
    bed_temp=40,
    print_speed=500,
    fan_percent=100
)

# Define design parameters
design_params = DesignParameters(
    inner_radius=15,
    height=40,
    skew_percent=10,
    star_tips=4,
    tip_length=5,
    bulge=2,
    nozzle_diameter=0.4,
    ripples_per_layer=50,
    ripple_depth=1,
    shape_factor=1.5
)

# Initialize print job
print_job = PrintJob(
    design_params=design_params,
    printer_settings=printer_settings,
    ripple_segs=2,
    first_layer_e_factor=0.4,
    centre_x=50,
    centre_y=50
)

# Generate the design
print_job.generate_steps()

# Preview the design
print_job.preview_design()

# Uncomment to generate and save gcode
# gcode = print_job.generate_gcode()
