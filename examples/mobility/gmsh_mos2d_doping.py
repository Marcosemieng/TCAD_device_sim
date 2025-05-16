# Copyright 2013 DEVSIM LLC
#
# SPDX-License-Identifier: Apache-2.0

# Import Libraries
import numpy as np
import matplotlib.pyplot as plt
from scipy.special import erfc
from scipy.optimize import curve_fit

### ----- ORIGINAL FORMULAS ----- ###

# Drain doping profile - equation: erfc diffusion (original)
def drain_doping_profile_original(params):
    """
    Generates the drain doping profile equation using the provided parameters.

    Parameters:
        params (dict): A dictionary containing the following keys:
            - drain_doping (float): The peak doping concentration.
            - x_gate_right (float): The x-coordinate of the gate's right edge.
            - x_diffusion_decay (float): The diffusion decay constant along the x-axis.
            - y_diffusion (float): The y-coordinate for diffusion.
            - y_diffusion_decay (float): The diffusion decay constant along the y-axis.

    Returns:
        str: The formatted drain doping profile equation.
    """
    return (
        "0.25*%(drain_doping)1.15e*erfc(-(x-%(x_gate_right)1.15e)/%(x_diffusion_decay)1.15e)*erfc(-(y-%(y_diffusion)1.15e)/%(y_diffusion_decay)1.15e)" % params
    )

# Drain doping profile - equation: erfc diffusion (original)
def source_doping_profile_original(params):
    """
    Generates the drain doping profile equation using the provided parameters.

    Parameters:
        params (dict): A dictionary containing the following keys:
            - drain_doping (float): The peak doping concentration.
            - x_gate_right (float): The x-coordinate of the gate's right edge.
            - x_diffusion_decay (float): The diffusion decay constant along the x-axis.
            - y_diffusion (float): The y-coordinate for diffusion.
            - y_diffusion_decay (float): The diffusion decay constant along the y-axis.

    Returns:
        str: The formatted drain doping profile equation.
    """
    return (
        "0.25*%(source_doping)1.15e*erfc((x-%(x_gate_left)1.15e)/%(x_diffusion_decay)1.15e)*erfc(-(y-%(y_diffusion)1.15e)/%(y_diffusion_decay)1.15e)" % params
    )

### ----- NEW FORMULAS ----- ###

# Lateral struggle decay factor calculations
# TO-DO: remove the X & Y from the function and either remove it completetly or make it automatic
def adjust_decay_factor(X, Y, center_x, radius_x, center_y, radius_y, rectangular_doping, doping_concentration, peak_doping_concentration, contact_length, diffusion_decay, initial_decay):
    """
    Adjusts the decay factor for the circular doping profile to match the vertical profile
    of rectangular_doping at x=contact_length with the vertical profile of doping_concentration
    at the next x-point after x=contact_length, only for y ≤ 0.

    Parameters:
        X (ndarray): 2D grid of x values.
        Y (ndarray): 2D grid of y values.
        rectangular_doping (ndarray): Rectangular doping profile.
        doping_concentration (ndarray): Circular doping profile.
        contact_length (float): The x-coordinate of the contact length.
        diffusion_decay (float): Diffusion decay constant.
        initial_decay (float): Initial value of decay_adj_circle.

    Returns:
        float: Adjusted decay factor.
    """
    # Define variable (temp, not sure if needed)
    doping_concentration_max = peak_doping_concentration
    
    # Find the index for x = contact_length and the next x-point
    x_index_contact = np.argmin(np.abs(X[0, :] - contact_length))  # Index for x = contact_length
    x_index_next = x_index_contact + 1  # Index for the next x-point after contact_length

    # Restrict to y ≤ 0
    y_mask = Y[:, 0] <= 0  # Mask for y ≤ 0
    y_values = Y[y_mask, 0]  # Extract y values for y ≤ 0

    # Extract vertical profiles for y ≤ 0
    vertical_profile_rectangular = rectangular_doping[y_mask, x_index_contact]
    vertical_profile_circular = doping_concentration[y_mask, x_index_next]

    # Define the model function for the circular doping profile
    def circular_doping_model(y, decay_adj_circle):
        # Use the index-based approach for distance calculation
        distance_from_center = np.sqrt(
            ((X[y_mask, x_index_next] - center_x) / radius_x) ** 2
            + ((y - center_y) / radius_y) ** 2
        )
        return_variable = doping_concentration_max * erfc((distance_from_center - 1) / (decay_adj_circle * diffusion_decay))
        return return_variable 

    # Perform curve fitting to optimize decay_adj_circle
    popt, _ = curve_fit(
        circular_doping_model,  # Model function
        y_values,              # y-axis values
        vertical_profile_rectangular,  # Target profile (rectangular doping)
        p0=[initial_decay],    # Initial guess for decay_adj_circle
        bounds=(0, np.inf)     # Ensure decay_adj_circle is positive
    )

    # Extract the optimized decay factor
    decay_adj_circle = popt[0]
    return decay_adj_circle

# TO-DO: WIP (look above)
# TO-DO:1) Make one for the Source & one for the Drain; 2) ...
def source_doping_profile_erfc(contact_length, junction_depth, overlap_length, doping_concentration_max, diffusion_decay):
    """
    Calculates the doping concentration for a rectangular and circular doping profile,
    adjusting the decay factor for the circular profile to ensure continuity.

    Parameters:
        contact_length (float): The x-coordinate of the contact length.
        junction_depth (float): The depth of the junction (y-coordinate).
        overlap_length (float): The overlap length for the doping profile.
        diffusion_decay (float): The diffusion decay constant.

    Returns:
        ndarray: The combined doping concentration profile.
    """
    # Define constants
    center_x = contact_length
    radius_x = abs(junction_depth)

    # Calculate parameters for the ellipse
    theta_end = round(np.arccos((overlap_length) / radius_x), 2)
    lateral_struggle = round(abs(junction_depth) / (radius_x * (1 - np.sin(theta_end))), 2)
    radius_y = radius_x * lateral_struggle
    center_y = junction_depth + radius_y

    # Define the x and y ranges (in meters)
    computation_length = 1.3 * (contact_length + overlap_length)
    x = np.linspace(-computation_length, computation_length, 500)  # x-axis range
    y = np.linspace(computation_length, -computation_length, 500)  # y-axis range

    # Create a 2D grid of x and y values
    X, Y = np.meshgrid(x, y)

    # Calculate the normalized distance from the center of the ellipse
    distance_from_center = np.sqrt(((X - center_x) / radius_x) ** 2 + ((Y - center_y) / radius_y) ** 2)

    # Calculate the angle (in radians) for each point in the grid
    angles = np.arctan2(Y - center_y, X - center_x)  # Angle in radians (-π to π)

    # Restrict the angles to the range 270° to 360° (or -π/2 to 0 in radians)
    mask = (angles >= -np.pi / 2) & (angles <= theta_end - np.pi / 2)

    # Restrict the doping concentration to y ≤ 0
    y_below_zero_mask = Y <= 0  # Mask for y ≤ 0

    # Combine the angle mask and the y ≤ 0 mask
    final_mask = mask & y_below_zero_mask

    # Doping profile for the rectangular grid
    rectangular_doping_mask = (X >= 0) & (X <= contact_length)
    rectangular_doping_final_mask = rectangular_doping_mask & y_below_zero_mask
    rectangular_doping = (
        doping_concentration_max
        * erfc(-(Y - junction_depth) / (diffusion_decay))
        * rectangular_doping_final_mask
    )

    # Doping profile for the circle grid
    doping_concentration = np.zeros_like(distance_from_center)  # Initialize with zeros
    decay_adj_circle = 0.011  # Initial decay factor for the circular doping profile
    doping_concentration[final_mask] = (
        doping_concentration_max 
        * erfc((distance_from_center[final_mask] - 1) / (decay_adj_circle * diffusion_decay))
    )

    # Adjust the decay factor
    decay_adj_circle = adjust_decay_factor(X, Y, center_x, radius_x, center_y, radius_y, rectangular_doping, doping_concentration, doping_concentration_max, contact_length, diffusion_decay, decay_adj_circle)

    # Update doping concentration with the adjusted decay factor
    doping_concentration[final_mask] = doping_concentration_max * erfc(
        (distance_from_center[final_mask] - 1) / (decay_adj_circle * diffusion_decay)
    )

    # Add the rectangular doping contribution
    doping_concentration += rectangular_doping

    return doping_concentration
