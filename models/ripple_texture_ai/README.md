# Ripple AI

This project generates 3D printable designs with ripple textures using AI. The designs are generated based on various parameters and can be previewed and converted to G-code for 3D printing.

## Project Structure

- `models/ripple_texture_ai/functions_template.py`: Contains the template function for calculating effects.
- `models/ripple_texture_ai/functions_generated.py`: Contains the generated function based on the template and prompt.
- `models/ripple_texture_ai/ripple_ai.py`: Main script for generating the ripple design, previewing it, and generating G-code.

## Dependencies

- Python 3.x
- `openai` library
- `fullcontrol` library

Install the required libraries using pip:

```sh
pip install openai fullcontrol
```

## Usage

1. **Define Printer Settings**: Configure the printer settings such as nozzle temperature, bed temperature, print speed, and fan percentage.

2. **Define Design Parameters**: Set the design parameters including inner radius, height, skew percentage, star tips, tip length, bulge, nozzle diameter, ripples per layer, ripple depth, and shape factor.

3. **Initialize Print Job**: Create a `PrintJob` instance with the defined design parameters and printer settings.

4. **Generate Steps**: Call the `generate_steps` method to generate the steps for the design.

5. **Preview Design**: Use the `preview_design` method to visualize the design.

6. **Generate G-code**: Uncomment and call the `generate_gcode` method to generate and save the G-code for 3D printing.


## License

This project is licensed under the MIT License.