# Copyright 2013 DEVSIM LLC
#
# SPDX-License-Identifier: Apache-2.0

import numpy as np

from devsim import node_model, set_parameter, solve, write_devices

from devsim.python_packages.simple_physics import GetContactBiasName, PrintCurrents
import diode_common

device = "diode2d"
region = "Bulk"

diode_common.Create2DGmshMesh(device, region)

# this is is the devsim format
write_devices(file="gmsh_diode2d_out.msh")

diode_common.SetParameters(device=device, region=region)

####
#### NetDoping
####
node_model(device=device, region=region, name="Acceptors", equation="1.0e18*step(0.5e-5-x);")
node_model(device=device, region=region, name="Donors", equation="1.0e18*step(x-0.5e-5);")
node_model(device=device, region=region, name="NetDoping", equation="Donors-Acceptors;")

diode_common.InitialSolution(device, region)

####
#### Initial DC solution
####
solve(type="dc", absolute_error=1.0, relative_error=1e-12, maximum_iterations=30)

###
### Drift diffusion simulation at equilibrium
###
diode_common.DriftDiffusionInitialSolution(device, region)

solve(type="dc", absolute_error=1e10, relative_error=1e-10, maximum_iterations=50)

####
#### Ramp the bias to 0.5 Volts
####
v = 0.0
v_max = 0.5 # MM
v_step = 0.01 # MM
# creating array for data conversion to numpy array (MM)
arr_v = np.zeros([int(v_max/v_step + 1)]) # MM
arr_i_top = np.zeros([int(v_max/v_step + 1)]) # MM
arr_i_bot = np.zeros([int(v_max/v_step + 1)]) # MM
i = 0  # MM
while v < v_max + 0.01:
    set_parameter(device=device, name=GetContactBiasName("top"), value=v)
    solve(type="dc", absolute_error=1e10, relative_error=1e-10, maximum_iterations=30)
    # PrintCurrents(device, "top")
    # PrintCurrents(device, "bot")
    top_iv = PrintCurrents(device, "top") # MM
    bot_iv = PrintCurrents(device, "bot") # MM
    print(top_iv, bot_iv)  # MM
    arr_v[i] = v # MM
    arr_i_top[i] = top_iv[1] # MM
    arr_i_bot[i] = bot_iv[1] # MM
    v += v_step
    i += 1  # MM
print(arr_v,arr_i_top,arr_i_bot) # MM

val = 10
for i in range(2):
    set_parameter(device=device, name=GetContactBiasName("top"), value=val)
    data = solve(
        type="dc",
        absolute_error=1e10,
        relative_error=1e-10,
        maximum_iterations=30,
        info=True,
    )
    print(data["converged"])
    if not data["converged"]:
        val = 0.6

print(data)
for i in data["iterations"]:
    for d in i["devices"]:
        for r in d["regions"]:
            for e in r["equations"]:
                print(e)

####
#### Export plots
####
write_devices(file="gmsh_diode2d.dat", type="tecplot")
write_devices(file="gmsh_diode2d_dd.msh", type="devsim")
write_devices(file="gmsh_diode2d.dat", type="vtk") # Paraview compatible
write_devices(file="gmsh_diode2d_dd.dat", type="vtk") # Paraview compatible
write_devices(file="gmsh_diode2d_out.dat", type="vtk") # Paraview compatible

####
#### Plot IV curve
####
# import matplotlib
# import matplotlib.pyplot
# matplotlib.pyplot.clf() # MM
# ivfields = ("IV_top",) # MM
# matplotlib.pyplot.plot(arr_v,arr_i_top) # MM
# matplotlib.pyplot.xlabel('V') # MM
# matplotlib.pyplot.ylabel('J (A/cm^2)') # MM
# matplotlib.pyplot.legend(ivfields) # MM
# matplotlib.pyplot.savefig("diode_2d_IV.png") # MM
