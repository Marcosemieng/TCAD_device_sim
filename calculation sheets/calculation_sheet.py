import numpy as np

# Input parameters
q = 1.6e-19  # coul
k = 1.3806503e-23  # J/K
T = 300 # K
#----------------------
eps_0 = 8.85e-14  # F/cm^2
eps_si = 11.1
eps_ox = 3.9 # 25 HfO
#----------------------
d = 5 * 1e-7  # cm
N_A = 1.0e17  # #/cm^3; body doping
N_D = 1.0e19  # #/cm^3, S/D doping
n_i = 1e10  # #/cm^3


# Calculated parameters
Vt = k*T/q # thermal voltage
Vbi = Vt * np.log((N_A * N_D) / (n_i*n_i))  # pn junction built-in potential
εox = eps_ox * eps_0
εs= eps_si * eps_0
#----------------------
Fb = k*T/q * np.log(N_A/n_i) # Eneregy difference between Fermi level and intrinsic Fermi level
Co = εox / d
# MOSFET: Max depletion channel width
Wm = np.sqrt((2 * εs * 2 * Fb) / (q * N_A))  # Max depletion width
# MOSFET: S/D junction width (no voltage applied)
Wj = np.sqrt(((2 * εs * Vbi)/q) * (1/N_A + 1/N_D))  # pn junction width   * np.log((1/N_A) + (1/N_D))
# MOSFET: threshold voltage
Vth = (np.sqrt(2 * εs * q * N_A * (2 * Fb)) / (Co)) + (2 * Fb)  # threshold voltage


# Print calculated parameters
print("Fb = ", Fb)
print("Co = ", Co)
print("Vbi = ", Vbi)
print("Wm = ", Wm) # cm
print("Wj = ", Wj) # cm
print("Vth = ", Vth)