# Import Libraries
import numpy as np
import matplotlib.pyplot as plt
from scipy.special import erfc
from scipy.optimize import curve_fit

# Lateral struggle decay factor calculations
# TO-DO: remove the X & Y from the function and either remove it completetly or make it automatic
def adjust_decay_factor(X, Y, center_x, radius_x, center_y, radius_y, rectangular_doping, doping_concentration, contact_length, diffusion_decay, initial_decay):
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
        return doping_concentration_max * erfc((distance_from_center - 1) / (decay_adj_circle * diffusion_decay))

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
def doping_profile_sd_erfc(contact_length, junction_depth, overlap_length, doping_concentration_max, diffusion_decay):
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
    decay_adj_circle = adjust_decay_factor(X, Y, center_x, radius_x, center_y, radius_y, rectangular_doping, doping_concentration, contact_length, diffusion_decay, decay_adj_circle)

    # Update doping concentration with the adjusted decay factor
    doping_concentration[final_mask] = doping_concentration_max * erfc(
        (distance_from_center[final_mask] - 1) / (decay_adj_circle * diffusion_decay)
    )

    # Add the rectangular doping contribution
    doping_concentration += rectangular_doping

    return doping_concentration

# This is a placholder function for the Gaussian doping profile
def doping_profile_sd_gaussian():
    return None

# Plot doping profile
def plot_doping_profile(X, Y, doping_profile_sd):
    """
    Plots the doping concentration profile.

    Parameters:
        X (ndarray): 2D grid of x values.
        Y (ndarray): 2D grid of y values.
        doping_profile_sd_erfc (ndarray): Doping concentration profile to be plotted.
    """
    plt.figure(figsize=(8, 6))
    contour = plt.contourf(X, Y, doping_profile_sd, levels=50, cmap="viridis")
    plt.colorbar(label="Doping Concentration (cm⁻³)")
    plt.title("Junction doping profile - Source")
    plt.xlabel("x (distance)")
    plt.ylabel("y (distance)")
    plt.gca().set_aspect('equal', adjustable='box')  # Ensure the aspect ratio is equal
    plt.grid(False)
    plt.show()


### ------ Test portion ------ ###


# Define S/D contact parameters
gate_length = 45  # Length of the gate; MM: default = 45
contact_length = 20  # Length of the contact; MM: default = 20
junction_depth = -10  # Junction depth; MM: default = -10
overlap_length = 0.1 * gate_length  # S/D to gate overlap length

# Define doping constants
diffusion_decay = 0.5  # Diffusion decay constant along the y axis
doping_concentration_max = 1e20  # Peak doping concentration

# Plot
computation_length = 1.3 * (contact_length + overlap_length)
x = np.linspace(- computation_length, computation_length, 500)  # x-axis range
y = np.linspace(computation_length, - computation_length, 500)  # y-axis range
X, Y = np.meshgrid(x, y)

doping_profile_sd_erfc_y = doping_profile_sd_erfc(contact_length, junction_depth, overlap_length, doping_concentration_max, diffusion_decay)
plot_doping_profile(X, Y, doping_profile_sd_erfc_y)
