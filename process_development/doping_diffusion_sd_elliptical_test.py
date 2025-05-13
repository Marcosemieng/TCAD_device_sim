import numpy as np
import matplotlib.pyplot as plt
from scipy.special import erfc

# Define S/D contact parameters
gate_length = 45  # Length of the gate
contact_length = 20
junction_depth = -10  # Junction depth
overlap_length = 0.1*gate_length  # S/D to gate overlap length (X2)

# Define constants
center_x = contact_length
radius_x = abs(junction_depth)

# Calculate parameters for the circle
theta_end = round(np.arccos((overlap_length) / radius_x), 2)
lateral_struggle = round(abs(junction_depth) / (radius_x * (1 - np.sin(theta_end))), 2)
radius_y = radius_x * lateral_struggle
center_y = junction_depth + (radius_y)
print(f"center_y: {center_y}")

# Define doping constants
diffusion_decay = 0.02  # Diffusion decay constant
doping_concentration_max = 1e20  # Maximum doping concentration

# Define the x and y ranges (in meters)
# x = np.linspace(center_x - 100.0, center_x + 100.0, 500)  # x-axis range
# y = np.linspace(center_y - 100.0, center_y + 100.0, 500)  # y-axis range
x = np.linspace(0, 25, 500)  # x-axis range
y = np.linspace(0, -25, 500)  # y-axis range

# Create a 2D grid of x and y values
X, Y = np.meshgrid(x, y)

# Calculate the normalized distance from the center of the ellipse
distance_from_center = np.sqrt(((X - center_x) / radius_x) ** 2 + ((Y - center_y) / radius_y) ** 2)

# Calculate the angle (in radians) for each point in the grid
angles = np.arctan2(Y - center_y, X - center_x)  # Angle in radians (-π to π)

# Restrict the angles to the range 270° to 360° (or -π/2 to 0 in radians)
# mask = (angles >= -np.pi / 2) & (angles <= 0)
mask = (angles >= -np.pi / 2) & (angles <= theta_end - np.pi / 2) 

# Calculate the doping concentration for the rectangular grid
rectangular_doping = (
    doping_concentration_max
    * erfc((X - contact_length) / (diffusion_decay))
    * erfc(-(Y - junction_depth) / (10*diffusion_decay))
)

# Apply the erfc function to model the doping concentration
doping_concentration = np.zeros_like(distance_from_center)  # Initialize with zeros
doping_concentration[mask] = 2 * doping_concentration_max * erfc((distance_from_center[mask] - 1) / (0.2*diffusion_decay))
doping_concentration += rectangular_doping  # Add the rectangular doping contribution
# doping_concentration = doping_concentration_max * erfc((distance_from_center - 1) / diffusion_decay)

# Plot the doping concentration
plt.figure(figsize=(8, 6))
contour = plt.contourf(X, Y, doping_concentration, levels=50, cmap="viridis")
plt.colorbar(label="Doping Concentration (cm⁻³)")
plt.title("Elliptical Doping Profile (270° to 360°) Using erfc")
plt.xlabel("x (m)")
plt.ylabel("y (m)")
plt.gca().set_aspect('equal', adjustable='box')  # Ensure the aspect ratio is equal
plt.grid(False)
plt.show()