# Copyright 2013 DEVSIM LLC
#
# SPDX-License-Identifier: Apache-2.0

import os # MM
import numpy as np # MM

# import libraries for conversion to excel (to be removed in the future) #MM
from pyexcel.cookbook import merge_all_to_a_book #MM
import glob #MM


import devsim as ds
from devsim.python_packages.simple_physics import GetContactBiasName, PrintCurrents

contactcharge_edge = "contactcharge_edge"
ece_name = "ElectronContinuityEquation"
hce_name = "HoleContinuityEquation"
celec_model = "(1e-10 + 0.5*abs(NetDoping+(NetDoping^2 + 4 * n_i^2)^(0.5)))"
chole_model = "(1e-10 + 0.5*abs(-NetDoping+(NetDoping^2 + 4 * n_i^2)^(0.5)))"


def rampbias(
    device,
    contact,
    end_bias,
    step_size,
    min_step,
    max_iter,
    rel_error,
    abs_error,
    callback,
):
    """
    Ramps bias with assignable callback function

    Uses devsim.get_parameter to get the bias currently at the contact being ramped.

    Parameters:
    -----------

    device : name of the device
    contact : contact name
    end_bias : bias for last step
    step_size : initial step size
    min_step : minimum step size
    max_iter : maximum number of iterations
    rel_error : required relative error for convergence
    abs_error : required absolute error for convergence
    callback : callback function that should be called on success.
               See printAllCurrents for an example.

    Description:
    ------------

    Uses GetContactBiasName to get the bias being applied at the contact specified.

    On each successfull bias, the callback function is called.

    Exceptions are raised if there is a failure at the last bias step attempted.

    """

    start_bias = ds.get_parameter(device=device, name=GetContactBiasName(contact))
    print("start bias is:", start_bias)
    if start_bias < end_bias:
        step_sign = 1
    else:
        step_sign = -1
    step_size = abs(step_size)

    last_bias = 0 # start_bias
    # creating array for data conversion to numpy array (MM)
    # arr_v = np.zeros([int(abs(end_bias)/step_size)]) # MM
    # arr_i = np.zeros([int(abs(end_bias)/step_size)]) # MM
    i = 0  # MM
    while abs(last_bias - end_bias) > min_step:
        print(("%s last end %e %e") % (contact, last_bias, end_bias))
        # Forcing first bias sep to be 0V (MM)
        if i ==0:
            next_bias = last_bias
            i += 1
        # Leaving here the code to run as usual beyond the first run (MM)    
        else:
            next_bias = last_bias + step_sign * step_size
        if next_bias < end_bias:
            next_step_sign = 1
        else:
            next_step_sign = -1

        if next_step_sign != step_sign:
            next_bias = end_bias
            print("setting to last bias %e" % (end_bias))
            print("setting next bias %e" % (next_bias))
        ds.set_parameter(
            device=device, name=GetContactBiasName(contact), value=next_bias
        )
        try:
            ds.solve(
                type="dc",
                absolute_error=abs_error,
                relative_error=rel_error,
                maximum_iterations=max_iter,
            )
            # assigning the voltage and current values to the array (MM)
            # test_iv = PrintCurrents(device, contact) # MM
            # print(test_iv)  # MM
            # arr_v[i] = next_bias # MM
            # arr_i[i] = test_iv[1] # MM
            # i += 1  # MM
        except ds.error as msg:
            if str(msg).find("Convergence failure") != 0:
                raise
            ds.set_parameter(
                device=device, name=GetContactBiasName(contact), value=last_bias
            )
            step_size *= 0.5
            print("setting new step size %e" % (step_size))
            if step_size < min_step:
                raise RuntimeError("Minimum step size too small")
            continue
        print("Succeeded")
        # print("V,I is:", arr_v, arr_i) # MM
        last_bias = next_bias
        callback(device)
    # Reset counter in case other sweeps are in the buffer #MM
    i = 0  # MM

    ####
    #### Plot IV curve
    ####
    # import matplotlib
    # import matplotlib.pyplot
    # matplotlib.pyplot.clf() # MM
    # ivfields = ("IV_MOSFET",) # MM
    # matplotlib.pyplot.plot(arr_v,arr_i) # MM
    # matplotlib.pyplot.xlabel('V') # MM
    # matplotlib.pyplot.ylabel('J (A/cm^2)') # MM
    # matplotlib.pyplot.legend(ivfields) # MM
    # matplotlib.pyplot.savefig("mosfet_2d_IV.png") # MM


def printAllCurrents(device):
    """
    Prints all contact currents on device
    """
    for c in ds.get_contact_list(device=device):
        PrintCurrents(device, c)
        # print("Print test:")  # MM
        # test_iv = PrintCurrents(device, c) # MM
        # print(test_iv)  # MM
    StoreCurrents_csv(device) # MM


# Store currents in csv file # MM
def StoreCurrents_csv(device):
    '''
       store contact currents in array
    '''
    # i = 0
    # for c in ['drain']:
        # if i == 0: # print only one current as they are duplicated apparently # MM
            #PrintCurrents(device, c)
    print("current c content is:", 'drain')
    # TODO add charge
    contact_bias_name = GetContactBiasName('drain')
    electron_current  = ds.get_contact_current(device=device, contact='drain', equation=ece_name)
    hole_current      = ds.get_contact_current(device=device, contact='drain', equation=hce_name)
    total_current     = electron_current + hole_current                                        
    Drain_voltage     = ds.get_parameter(device=device, name=GetContactBiasName('drain'))
    Gate_voltage      = ds.get_parameter(device=device, name=GetContactBiasName('gate'))
    data = (Gate_voltage,Drain_voltage, electron_current, hole_current, total_current)
    print(data)
    with open("id_vds.csv", "a", encoding="utf-8") as ofh:
        # Check if the file is empty or doesn't exist (MM)
        if os.stat("id_vds.csv").st_size == 0: #(MM)
            # Write the header row (MM)
            ofh.write("Title,Vgs,Vds,Ids\n")
        # Write the data row
        ofh.write('%s,%s,%s,%s\n' % ('Id@V',Gate_voltage,Drain_voltage,electron_current))
        # i += 1; 
    merge_all_to_a_book(glob.glob("id_vds.csv"), "id_vds.xlsx")
