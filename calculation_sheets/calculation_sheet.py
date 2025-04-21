# This '.py' file is used to calculate the parameters of a MOSFET device by rule of thumb based on academic formulas.

import numpy as np

# Import 'sys' and 'os' in order to use modules from other parallel packages
# import sys
# import os
# sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

# import device_characterisation.mosfet_char as mosfet_char


# Input parameters
q = 1.6e-19  # coul
k = 1.3806503e-23  # J/K
T = 300 # K
#----------------------
eps_0 = 8.85e-14  # F/cm^2
eps_si = 11.1
eps_ox = 3.9 # 25 HfO
#----------------------
d = 20 * 1e-7  # cm; oxide thickness
tch = 10 * 1e-7 # cm; semiconductor thickness
l = 500 * 1e-7 # cm; semiconductor channel length
N_A = 1.0e12  # #/cm^3; body doping
N_D = 1.0e20  # #/cm^3, S/D doping
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
Vth_ass = -1.6 # assumed thresold voltage
# MOSFET BG: carrier concentraion
Vgs = 10
n2D = Co*(Vgs-Vth)/q 
# n2D_ass = Co*(Vgs-Vth_ass)/q # carrier concantration based on a virtual Vgs
n2D_ass = 2.8e+12 # just for manual insertion
n1D_ass = np.sqrt(n2D_ass)
n3D_ass = n2D_ass * n1D_ass
# MOSFET rsh sheet resistance (TLM)
l_um = l * 1e4 # channel length converted from cm to um
rsh = 20 * 1e3 # slope of TLM in Ohm/sqr
# MOSFET uch channel mobility (TLM)
uch = (1/q) * (1/(n3D_ass * tch * rsh))


# Print calculated parameters
print("Fb = ", Fb)
print("Co = ", Co)
print("Vbi = ", Vbi)
print("Wm = ", Wm) # cm
print("Wj = ", Wj) # cm
print("Vth = ", Vth)
print(f"n2D = {n2D:.2e}") # cm^-2
print(f"n2D_ass = {n2D_ass:.2e}") # cm^-2
print(f"n3D_ass = {n3D_ass:.2e}") # cm^-3
print("Lch = ", l_um)
print("Rsh = ", rsh)
print("uch = ", uch)

# mosfet_ion = mosfet_char.mosfet_ion_char('/Users/macbookpro/Desktop/id_vds.csv')
# print("Ion = ", mosfet_ion)