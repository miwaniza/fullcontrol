from math import cos, sin, tau

def calculate_effects(params, t_val):
	ripple_effect = params['ripple_depth'] * (0.5 + (0.5 * cos((params['ripples_per_layer'] + 0.5) * (t_val * tau))))
	tip_effect = params['tip_length'] * (0.5 - 0.5 * cos(params['star_tips'] * (t_val * tau))) ** params['shape_factor']
	bulge_effect = params['bulge'] * sin((params['centre_now_z'] / params['height']) * (0.5 * tau))
	result = params['inner_radius'] + ripple_effect + tip_effect + bulge_effect
	return result