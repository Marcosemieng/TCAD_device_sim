import numpy as np
import matplotlib.pyplot as plt

def adjust_circle_center_y(contact_length, junction_depth, radius, lateral_struggle):
    """
    Adjusts the center_y of the circle so that the last point of the line
    and the first point of the circle are concatenated.
    """
    # Calculate the last point of the line
    line_last_x = contact_length
    line_last_y = junction_depth

    # Calculate the first point of the circle
    theta_start = 3 * np.pi / 2  # Starting angle of the circle (270°)
    circle_first_x = contact_length + radius * np.cos(theta_start)
    circle_first_y = lateral_struggle * radius * np.sin(theta_start)  # Initial center_y is 0

    # Adjust center_y so that the circle's first point matches the line's last point
    center_y_adjusted = line_last_y - circle_first_y
    return center_y_adjusted

def calculate_theta_end(center_y, radius, lateral_struggle):
    """
    Calculates the ending angle (theta_end) for the circle segment so that it stops at y = 0.
    """
    # Solve for the angle where the circle's y-coordinate equals 0
    theta_end = np.arcsin(-center_y / (lateral_struggle * radius))
    return theta_end

# Input parameters
contact_length = 30  # S/D contact Length (X1)
junction_depth = -5  # Junction depth

gate_legth = 50  # Length of the gate
overlap_length = 0.1 * gate_legth  # S/D to gate overlap length (X2)

lateral_struggle = 10  # Lateral struggle (it should be 0.8, but it is for a Gaussian, not for a circle)

### ---------- ###

# Adjust the circle's center_y
radius = 1  # Radius of the circle; abs(junction_depth)
center_y = adjust_circle_center_y(contact_length, junction_depth, radius, lateral_struggle)

# Calculate the ending angle (theta_end)
theta_end = calculate_theta_end(center_y, radius, lateral_struggle)
print("theta_end is:", theta_end)

# Define the circle parameters
center_x = contact_length  # X-coordinate of the circle's center

# Generate points for the circle (from 270° to theta_end)
theta = np.linspace(-np.pi / 2, theta_end, 500)  # Angle values from 270° to theta_end to stop at y=0
circle_x = center_x + radius * np.cos(theta)  # X-coordinates of the circle
circle_y = center_y + (lateral_struggle * radius) * np.sin(theta)  # Y-coordinates of the circle

### ---------- ###

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
plt.title("Line and Circle Segment Plot")
plt.xlabel("X")
plt.ylabel("Y")
plt.axhline(0, color='gray', linestyle='--', linewidth=0.5)  # X-axis
plt.axvline(0, color='gray', linestyle='--', linewidth=0.5)  # Y-axis
plt.grid(True)
plt.legend()
plt.show()