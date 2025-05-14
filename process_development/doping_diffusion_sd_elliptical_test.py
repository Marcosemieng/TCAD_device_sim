import numpy as np
import matplotlib.pyplot as plt
from scipy.special import erfc
from scipy.optimize import curve_fit

# Define S/D contact parameters
gate_length = 45  # Length of the gate
contact_length = 20
junction_depth = -10  # Junction depth
overlap_length = 0.1 * gate_length  # S/D to gate overlap length (X2)

# Define doping constants
diffusion_decay = 0.9  # Diffusion decay constant
doping_concentration_max = 1e20  # Maximum doping concentration

### --------- ###
### --------- ###

# Define constants
center_x = contact_length
radius_x = abs(junction_depth)

# Calculate parameters for the ellipse
theta_end = round(np.arccos((overlap_length) / radius_x), 2)
lateral_struggle = round(abs(junction_depth) / (radius_x * (1 - np.sin(theta_end))), 2)
radius_y = radius_x * lateral_struggle
center_y = junction_depth + radius_y
print(f"center_y: {center_y}")

# Define the x and y ranges (in meters)
x = np.linspace(0, 25, 500)  # x-axis range
y = np.linspace(0, -25, 500)  # y-axis range

# Create a 2D grid of x and y values
X, Y = np.meshgrid(x, y)

# Calculate the normalized distance from the center of the ellipse
distance_from_center = np.sqrt(((X - center_x) / radius_x) ** 2 + ((Y - center_y) / radius_y) ** 2)

# Calculate the angle (in radians) for each point in the grid
angles = np.arctan2(Y - center_y, X - center_x)  # Angle in radians (-π to π)

# Restrict the angles to the range 270° to 360° (or -π/2 to 0 in radians)
mask = (angles >= -np.pi / 2) & (angles <= theta_end - np.pi / 2)

### --------- ###
### --------- ###

# Doping profile for the rectangular grid
rectangular_doping_mask = (X >= 0) & (X <= contact_length)
rectangular_doping = (
    doping_concentration_max
    * erfc(-(Y - junction_depth) / (diffusion_decay))
    * rectangular_doping_mask
)

### --------- ###
### --------- ###

# Doping profile for the circle grid
doping_concentration = np.zeros_like(distance_from_center)  # Initialize with zeros
decay_adj_circle = 0.011  # Initial decay factor for the circular doping profile
print(f"Original decay factor: {decay_adj_circle}")
doping_concentration[mask] = doping_concentration_max * erfc((distance_from_center[mask] - 1) / (decay_adj_circle * diffusion_decay))

# Function to adjust decay_adj_circle using an index-based approach
def adjust_decay_factor(X, Y, rectangular_doping, doping_concentration, contact_length, diffusion_decay, initial_decay):
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

# Adjust the decay factor
decay_adj_circle = adjust_decay_factor(X, Y, rectangular_doping, doping_concentration, contact_length, diffusion_decay, decay_adj_circle)
print(f"Adjusted decay factor: {decay_adj_circle}")

# Update doping concentration with the adjusted decay factor
doping_concentration[mask] = doping_concentration_max * erfc((distance_from_center[mask] - 1) / (decay_adj_circle * diffusion_decay))

### --------- ###

# Add the rectangular doping contribution
doping_concentration += rectangular_doping

### --------- ###

# Plot the doping concentration
plt.figure(figsize=(8, 6))
contour = plt.contourf(X, Y, doping_concentration, levels=50, cmap="viridis")
plt.colorbar(label="Doping Concentration (cm⁻³)")
plt.title("Elliptical Doping Profile with Adjusted Decay Factor (y ≤ 0)")
plt.xlabel("x (m)")
plt.ylabel("y (m)")
plt.gca().set_aspect('equal', adjustable='box')  # Ensure the aspect ratio is equal
plt.grid(False)
plt.show()