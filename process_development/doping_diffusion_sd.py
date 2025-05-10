import numpy as np
import matplotlib.pyplot as plt
from scipy.special import erfc

# Define constants (values from the provided code)
drain_doping = 1e20
x_gate_right = 30e-7 # cm
# x_diffusion_decay = 8.48*1e-8 # T=1000C; t=1hr; (TBD)
x_diffusion_decay = 8.48*1e-8 # T=1000C; t=1hr; (TBD)
y_diffusion = 800*1e-7
# y_diffusion_decay = 8.48*1e-6 # cm T=1000C; t=1hr; (From Sze example pg. 473)
y_diffusion_decay = 10*1e-8 # cm

# Define the x and y ranges (in meters)
x = np.linspace(2.5e-6, 3.5e-6, 500)  # x-axis range around x_gate_right
y = np.linspace(0.5e-5, 100e-6, 500)  # y-axis range around y_diffusion

# Create a 2D grid of x and y values
X, Y = np.meshgrid(x, y)

# Calculate the doping concentration using the formula
doping_concentration = (
    drain_doping
    # * erfc((X - x_gate_right) / (2 * x_diffusion_decay))
    * erfc((X - x_gate_right) / (0.8 * x_diffusion_decay))
    * erfc(-(Y - y_diffusion) / (50*y_diffusion_decay))
)

# Plot the doping concentration
plt.figure(figsize=(8, 6))
contour = plt.contourf(X, Y, doping_concentration, levels=50, cmap="viridis")
# contour = plt.contourf(Y, doping_concentration, levels=50, cmap="viridis")
# plt.plot(y, doping_concentration)
plt.axis([2.5e-6, 3.5e-6, 0, 100e-6])


# plt.title("1D Drain Doping Concentration Profile")
# plt.xlabel("y (cm)")
# plt.ylabel("Doping Concentration (cm⁻³)")
# plt.legend()
# plt.grid(True)
# plt.show()


plt.colorbar(label="Doping Concentration (cm⁻³)")
plt.title("Drain Doping Concentration Profile")
plt.xlabel("x (m)")
plt.ylabel("y (m)")
plt.grid(False)
plt.show()