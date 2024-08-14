from math import cos, sin, tau, sqrt

def calculate_effects(params, t_val):
    # Trefoil knot parameters
    trefoil_radius = params['inner_radius']
    a = 0.5 * trefoil_radius
    b = trefoil_radius
    
    # Calculate trefoil knot position
    x = a * sin(t_val * tau) + b * sin(2 * (t_val * tau))
    y = a * cos(t_val * tau) - b * cos(2 * (t_val * tau))
    z = -b * sin(3 * (t_val * tau))
    
    # Base radius
    radial_position = sqrt(x**2 + y**2)

    # Additional effects
    ripple_effect = params['ripple_depth'] * (0.5 + (0.5 * cos((params['ripples_per_layer'] + 0.5) * (t_val * tau))))
    tip_effect = params['tip_length'] * (0.5 - 0.5 * cos(params['star_tips'] * (t_val * tau))) ** params['shape_factor']
    bulge_effect = params['bulge'] * sin((params['centre_now_z'] / params['height']) * (0.5 * tau))
    
    # Final radius with all effects applied
    result = radial_position + ripple_effect + tip_effect + bulge_effect
    return result