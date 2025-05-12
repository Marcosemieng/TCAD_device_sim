import numpy as np
import matplotlib.pyplot as plt


# Define S/D geometry parameters
gate_length = 45  # Length of the gate
contact_length = 20
junction_depth = -10  # Junction depth
overlap_length = 0.1*gate_length  # S/D to gate overlap length (X2)

# Define geometry parameters
center_x = contact_length
radius_x = abs(junction_depth)

# Calculate parameters for the circle
test_cos = ((overlap_length - center_x) / radius_x) # 

# TO-DO: understand whats the relationship with the phase 
theta_end = round(np.arccos((overlap_length) / radius_x), 2)
lateral_struggle = round(abs(junction_depth) / (radius_x * (1 - np.sin(theta_end))), 2)
center_y = junction_depth + (radius_x * lateral_struggle)


# Generate points for the circle (from 270° to theta_end)
theta = np.linspace(-np.pi / 2, -theta_end, 500)  # Angle values from 270° to theta_end to stop at y=0
circle_x = center_x + radius_x * np.cos(theta)  # X-coordinates of the circle
circle_y = center_y + (lateral_struggle * radius_x) * np.sin(theta)  # Y-coordinates of the circle

# Generate points for the horizontal line
line_x = np.linspace(0, contact_length, 500)  # X-coordinates from 0 to contact_length
line_y = np.full_like(line_x, junction_depth)  # Y-coordinates are constant (same as the starting y of the circle)


# Plot the circle segment
plt.figure(figsize=(8, 6))
plt.plot(circle_x, circle_y) # plt.plot(circle_x, circle_y, label="Circle Segment (270° to theta_end)")

# Plot the horizontal line
plt.plot(line_x, line_y) # plt.plot(line_x, line_y, label="Horizontal Line (x=0 to x=2)")

# Customize the plot
plt.gca().set_aspect('equal', adjustable='box')  # Ensure the aspect ratio is equal
plt.title("Circle Segment Plot")
plt.xlabel("X")
plt.ylabel("Y")
plt.axhline(0, color='gray', linestyle='--', linewidth=0.5)  # X-axis
plt.axvline(0, color='gray', linestyle='--', linewidth=0.5)  # Y-axis
plt.grid(True)
plt.legend()
plt.show()