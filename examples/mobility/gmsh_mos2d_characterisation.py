# This '.py' file serves the sole purpose of side dvelopment
# The used file must go in 'examples/mobility/gmsh_mos2d_characterisation.py'

import os
import csv
import numpy as np

import devsim.python_packages.simple_physics as simple_physics
import gmsh_mos2d_create as gmsh_mos2d_create

# Function to extract Ion (Vg=Vd) from Id@Vg at Vds=Vdd=1V
def ion(file_path):
    Vds_bias = 1  # Vds=1V bias value to filter the data: data must be extracted at this Vds=Vdd=1V
    voltages = []
    currents = []

    # Open the CSV file and read the data
    with open(file_path, mode='r', encoding='utf-8') as csv_file:
        reader = csv.DictReader(csv_file)  # Use DictReader to access columns by name
        for row in reader:
            try:
                # Process only rows where Vds == Vds_bias
                if (float(row['Vds']) == Vds_bias) & (row['Title'] == 'Id@V_gate_bias'):
                    voltages.append(float(row['Vgs']))
                    currents.append(float(row['Ids']))
            except KeyError:
                print("Error: Required columns ('Vgs', 'Vds', 'Ids') not found in the CSV file.")
                return None
            except ValueError:
                print("Error: Invalid data in 'Vgs' or 'Vds' or 'Ids' columns.")
                return None

    # Convert lists to NumPy arrays
    voltages = np.array(voltages)
    currents = np.array(currents)

    # Use NumPy's interpolation to extrapolate current at Vgs = 0 and Vgs = 1
    current_at_1 = np.interp(1, voltages, currents)
    return current_at_1


# Function to extract Ioff (Vg=0) from Id@Vg at Vds=Vdd=1V
def ioff(file_path):
    Vds_bias = 1  # Vds=1V bias value to filter the data: data must be extracted at this Vds=Vdd=1V
    voltages = []
    currents = []

    # Open the CSV file and read the data
    with open(file_path, mode='r', encoding='utf-8') as csv_file:
        reader = csv.DictReader(csv_file)  # Use DictReader to access columns by name
        for row in reader:
            try:
                # Process only rows where Vds == Vds_bias
                if (float(row['Vds']) == Vds_bias) & (row['Title'] == 'Id@V_gate_bias'):
                    voltages.append(float(row['Vgs']))
                    currents.append(float(row['Ids']))
            except KeyError:
                print("Error: Required columns ('Vgs', 'Vds', 'Ids') not found in the CSV file.")
                return None
            except ValueError:
                print("Error: Invalid data in 'Vgs' or 'Vds' or 'Ids' columns.")
                return None

    # Convert lists to NumPy arrays
    voltages = np.array(voltages)
    currents = np.array(currents)

    # Use NumPy's interpolation to extrapolate current at Vgs = 0 and Vgs = 1
    current_at_0 = np.interp(0, voltages, currents)
    return current_at_0


# Function to extract Ion/Ioff ratio from Id@Vg at Vds=Vdd=1V
def ion_off_ratio(file_path):
    # Get the I_on and I_off values
    i_on = ion(file_path)
    i_off = ioff(file_path)

    # Ensure both values are valid
    if i_on is None or i_off is None or i_off == 0:
        print("Error: Invalid I_on or I_off values.")
        return None

    # Calculate the ratio
    on_off_ratio = i_on / i_off
    return on_off_ratio


# Function to extract Imax (Vg=Vd) from Id@Vg at Vds=Vdd=1.5V
def imax(file_path):
    Vds_bias = 1  # Vds=1V bias value to filter the data: data must be extracted at this Vds=Vdd=1V
    voltages = []
    currents = []

    # Open the CSV file and read the data
    with open(file_path, mode='r', encoding='utf-8') as csv_file:
        reader = csv.DictReader(csv_file)  # Use DictReader to access columns by name
        for row in reader:
            try:
                # Process only rows where Vds == Vds_bias
                if (float(row['Vds']) == Vds_bias) & (row['Title'] == 'Id@V_gate_bias'):
                    voltages.append(float(row['Vgs']))
                    currents.append(float(row['Ids']))
            except KeyError:
                print("Error: Required columns ('Vgs', 'Vds', 'Ids') not found in the CSV file.")
                return None
            except ValueError:
                print("Error: Invalid data in 'Vgs' or 'Vds' or 'Ids' columns.")
                return None

    # Convert lists to NumPy arrays
    voltages = np.array(voltages)
    currents = np.array(currents)

    # Use NumPy's interpolation to extrapolate current at Vgs = 0 and Vgs = 1.5
    current_at_1 = np.interp(1.5, voltages, currents)
    return current_at_1


# Function to extract Imin (Vg=-3V) from Id@Vg at Vds=Vdd=0.1V
def imin(file_path):
    Vds_bias = 0.1  # Vds=1V bias value to filter the data: data must be extracted at this Vds=Vdd=1V; Updated to take it at Vds=0.1V
    voltages = []
    currents = []

    # Open the CSV file and read the data
    with open(file_path, mode='r', encoding='utf-8') as csv_file:
        reader = csv.DictReader(csv_file)  # Use DictReader to access columns by name
        for row in reader:
            try:
                # Process only rows where Vds == Vds_bias
                if (float(row['Vds']) == Vds_bias) & (row['Title'] == 'Id@V_gate_bias'):
                    voltages.append(float(row['Vgs']))
                    currents.append(float(row['Ids']))
            except KeyError:
                print("Error: Required columns ('Vgs', 'Vds', 'Ids') not found in the CSV file.")
                return None
            except ValueError:
                print("Error: Invalid data in 'Vgs' or 'Vds' or 'Ids' columns.")
                return None

    # Convert lists to NumPy arrays
    voltages = np.array(voltages)
    currents = np.array(currents)

    # Use NumPy's interpolation to extrapolate minimum current at Vgs=-3V and Vds=0.1V from the Id@Vgs
    current_at_min_Vg = np.interp(-3, voltages, currents)
    return current_at_min_Vg


# Function to extract Imax/Imin ratio from Id@Vg at Vds=Vdd=1V
# this is done as these devices to not have a fixed Vth = 0
def imax_min_ratio(file_path):
    # Get the I_on and I_off values
    i_max = imax(file_path)
    i_min = imin(file_path)

    # Ensure both values are valid
    if i_max is None or i_min is None or i_min == 0:
        print("Error: Invalid I_on or I_off values.")
        return None

    # Calculate the ratio
    ion_off_ratio = i_max / i_min
    return ion_off_ratio


# Function to extract the threshold voltage Vth from Id@Vg at Vds=Vdd=1V, by ELR method
def Vth_ELR(file_path, Vds_bias=1):
    # Vds_bias = 1  # Vds=1V bias value to filter the data: data must be extracted at this Vds=Vdd=1V
    voltages = []
    currents = []

    # Open the CSV file and read the data
    with open(file_path, mode='r', encoding='utf-8') as csv_file:
        reader = csv.DictReader(csv_file)  # Use DictReader to access columns by name
        for row in reader:
            try:
                # Process only rows where Vds == Vds_bias
                if (float(row['Vds']) == Vds_bias) & (row['Title'] == 'Id@V_gate_bias'):
                    voltages.append(float(row['Vgs']))
                    currents.append(float(row['Ids']))
            except KeyError:
                print("Error: Required columns ('Vgs', 'Vds', 'Ids') not found in the CSV file.")
                return None
            except ValueError:
                print("Error: Invalid data in 'Vgs' or 'Vds' or 'Ids' columns.")
                return None

    # Convert lists to NumPy arrays
    voltages = np.array(voltages)
    currents = np.array(currents)

    # Calculate the first derivative using NumPy's gradient function
    derivatives = np.gradient(currents, voltages)

    # Find the maximum derivative and the corresponding voltage
    gm_peak = np.max(derivatives)
    index_gm_peak = np.argmax(derivatives)
    voltage_at_gm_peak = voltages[index_gm_peak]
    current_at_gm_peak = currents[index_gm_peak]

    # Find the intersect along the x-axis
    slope = derivatives[index_gm_peak]
    v_intersect = voltage_at_gm_peak - (current_at_gm_peak / slope)

    # Find Vth: gm_peak method
    v_th = v_intersect - (Vds_bias/2)

    return gm_peak, voltage_at_gm_peak, v_intersect, v_th


# Function to extract the threshold voltage Vth from Id@Vg at Vds=Vdd=1V, by 'constant current' method
def Vth_CC(file_path, Vds_bias=1):
    # Vds_bias = 1  # Vds=1V bias value to filter the data: data must be extracted at this Vds=Vdd=1V
    voltages = []
    currents = []

    # Open the CSV file and read the data
    with open(file_path, mode='r', encoding='utf-8') as csv_file:
        reader = csv.DictReader(csv_file)  # Use DictReader to access columns by name
        for row in reader:
            try:
                # Process only rows where Vds == Vds_bias
                if (float(row['Vds']) == Vds_bias) & (row['Title'] == 'Id@V_gate_bias'):
                    voltages.append(float(row['Vgs']))
                    currents.append(float(row['Ids']))
            except KeyError:
                print("Error: Required columns ('Vgs', 'Vds', 'Ids') not found in the CSV file.")
                return None
            except ValueError:
                print("Error: Invalid data in 'Vgs' or 'Vds' or 'Ids' columns.")
                return None

    # Convert lists to NumPy arrays
    voltages = np.array(voltages)
    currents = np.array(currents)

    # Find Vth: constant current method
    voltage_at_target_current = None
    target_current = 1e-9  # TO-DO: convert in A/cm value - (Vgs=Vth@Ids=1.810-9 (A/um)) 
    if target_current is not None:
        try:
            voltage_at_target_current = np.interp(target_current, currents, voltages)
        except ValueError:
            print("Error: Target current is out of range.")
            voltage_at_target_current = None

    return voltage_at_target_current


# Function to extract the Subthreshold swing (SS) from Id@Vg at Vds=Vdd=1V
# This function uses the Vth value calculated by mosfet_Vth_char
# and the slope at Vth to calculate the subthreshold swing.
# TO-DO: modify it to work based on the Vth value calculated by the 'constant current' method
def SS(file_path):
    # Extract voltages and currents from the CSV file
    Vds_bias = 1  # Vds=1V bias value to filter the data
    voltages = []
    currents = []

    # Call mosfet_Vth_char to get v_th
    _, _, _, v_th = Vth_ELR(file_path, Vds_bias = 1)

    if v_th is None:
        print("Error: Unable to calculate Vth.")
        return None

    with open(file_path, mode='r', encoding='utf-8') as csv_file:
        reader = csv.DictReader(csv_file)
        for row in reader:
            try:
                if float(row['Vds']) == Vds_bias:
                    voltages.append(float(row['Vgs']))
                    currents.append(float(row['Ids']))
            except KeyError:
                print("Error: Required columns ('Vgs', 'Vds', 'Ids') not found in the CSV file.")
                return None
            except ValueError:
                print("Error: Invalid data in 'Vgs', 'Vds', or 'Ids' columns.")
                return None

    # Convert lists to NumPy arrays
    voltages = np.array(voltages)
    currents = np.array(currents)

    # Convert currents to log scale
    currents_log = np.log10(currents)

    # Calculate the first derivative (slope) using NumPy's gradient function
    derivatives = np.gradient(currents_log, voltages)

    # Find the index of the closest voltage to v_th
    index_v_th = (np.abs(voltages - v_th)).argmin()

    # Get the slope at v_th - 0.24V (arbitrary number, see how is it considered)
    # TO-DO: Make it rigourus to find the minimum and calculate slope in the middle of it
    correction_index = 0.24 # This must be calculated rigorously
    v_th_corrected = v_th - correction_index
    index_v_th_corrected = (np.abs(voltages - v_th_corrected)).argmin()

    # Get the slope at v_th and the corrected slope
    slope_at_v_th = derivatives[index_v_th]
    slope_at_v_th_corrected = derivatives[index_v_th_corrected]

    # Subthreshold swing calculation
    ss = 1/slope_at_v_th_corrected

    return slope_at_v_th, ss


# Function to extract the Field Effect Mobility from Id@Vg
# This function is a placeholder and needs to be implemented based on the specific mobility calculation method.
# uFE = (Lch * gm) / (Wch * Cins * Vds); Cins = gate insulator capacitance; Vds = ?; Wch = ?.
def mobility_fe(file_path, Lch=None, Wch=None, Cins=None):
    # calculate gm_peak
    gm_peak, _, _, _ = mosfet_Vth_char(file_path)

    # TO-DO: these numbers below should be given externally rigorously
    eps_0 = 8.85e-14  # F/cm^2
    eps_ox = 3.9 # 25 HfO
    εox = eps_ox * eps_0
    d = 10 * 1e-7  # cm
    Cins = εox / d
    Lch = 45e-7  # cm
    Wch = 1e-7  # cm (for now just approximated as in reality the width is virtually 0)
    Vds_bias = 1  # Vds=1V bias

    # Calculate the field effect mobility
    # TO-DO: Check if the units are consistent
    uFE = (Lch * gm_peak) / (Wch * Cins * Vds_bias)

    return uFE


# Function to extract the DIBL (Drain Induced Barrier Lowering) from Id@Vg
# This function is a placeholder and needs to be implemented based on the specific DIBL calculation method.
# It needs to run across two sets of Vds: = 1V and = 0.1V, extract Vth for both
# DIBL = Vth(Vds=1V) - Vth(Vds=0.1V)/(Vds=1V - Vds=0.1V)
# Vth is extracted by the 'constant current method'
def DIBL(file_path):

    # Call mosfet_Vth_char to get v_th
    Vds_bias_high = 1
    Vds_bias_low = 0.1
    v_th_1V = Vth_CC(file_path, Vds_bias = Vds_bias_high)
    v_th_100mV = Vth_CC(file_path, Vds_bias = Vds_bias_low)
    # _, _, _, v_th_1V = Vth_ELR(file_path, Vds_bias = Vds_bias_high)
    # _, _, _, v_th_100mV = Vth_ELR(file_path, Vds_bias = Vds_bias_low)

    if (v_th_1V is None) or (v_th_100mV is None):
        print("Error: Unable to calculate Vth.")
        return None
    
    # Calculate DIBL
    dibl = v_th_1V - v_th_100mV/(Vds_bias_high - Vds_bias_low)

    return dibl


# Function to extract rds from Id@Vd at Vds=x (This is a meta function)
def rds_arbitrary(file_path,Vds=0.1,Vgs=1):
    rds = None
    
    voltages = []
    currents = []

    # Open the CSV file and read the data
    with open(file_path, mode='r', encoding='utf-8') as csv_file:
        reader = csv.DictReader(csv_file)  # Use DictReader to access columns by name
        for row in reader:
            try:
                # Process only data of Id@Vds for Vgs=xV 
                if (float(row['Vgs']) == Vgs) & (row['Title'] == 'Id@V_drain_bias'):
                    voltages.append(float(row['Vds']))
                    currents.append(float(row['Ids']))
            except KeyError:
                print("Error: Required columns ('Vgs', 'Vds', 'Ids') not found in the CSV file.")
                return None
            except ValueError:
                print("Error: Invalid data in 'Vgs' or 'Vds' or 'Ids' columns.")
                return None

    # Convert lists to NumPy arrays
    voltages = np.array(voltages)
    currents = np.array(currents)

    # Use NumPy's interpolation to extrapolate current at Vds = 0.1 and Vgs = xV
    current_at = np.interp(Vds, voltages, currents)

    # Calculate the resistance
    rds = Vds / current_at

    return rds


# Function to extract Rtot from Id@Vds
# This function is a placeholder and needs to be implemented based on the specific resistance calculation method.
# Methodology: Rtot is extracted at Vds=0.1V (linear region)
# Steps: 
# 1) From Id@Vgs (Vds=1v) find the threshold voltage by which Vgs=Vth@Ids=1.810-9 (A/um); 
# 2) Find two overdrive voltages (Vov = Vgs - Vth) to obtain a min & max carrier density of n2D=1e^12 & 1e^13 (Mos2 specific), 
# by the formula: n2D = Co*(Vgs-Vth)/q; Translate it into Vgs voltages needed.
# 3) (OPTIONAL) Make sure those Id@Vds curves are available in that range of overdrive voltages (might need to add additional
# steps in the Id@Vds simulations @Vgs_overdrive_targets)
# 4) Extract the current of Id@Vds at Vds=0.1V (linear region) and calculate the resistance as Rtot = Vds/Id
# Do it for the two different overdirve voltages
# Temporary: for now is calculated only at one overdrive voltage (fixed at Vov = Vgs=1V - Vth)
def r_tot(file_path,Vds=0.1,Vgs=1):

    Rtot = None

    # Define consants
    q = 1.6e-19 # C (charge of an electron)
    eps_0 = simple_physics.eps_0 # F/cm^2 (vacuum permittivity)
    eps_ox = simple_physics.eps_ox  # oxide permittivity
    εox = eps_ox * eps_0
    # TO-DO: this should be given externally
    d = gmsh_mos2d_create.oxide_thickness # # cm (back gate oxide thickness)

    # Define MoS2 min & max carrier concentration
    n2D_min = 1e12 # cm^-2 (minimum carrier concentration)
    n2D_max = 1e13 # cm^-2 (maximum carrier concentration)

    # Define back gate oxide capacitance
    Co = εox / d # modify it, this is just a plce holder

    # Call mosfet_Vth_CC to get the threshold voltage Vth by the constant 'current method'
    v_th = Vth_CC(file_path, Vds_bias = 1)

    # Find the Vgs voltages dictaded by the min & max carrier concentration in MoS2 (typical ones)
    # Place holder function for when double overdrive voltage will be used
    Vgs_min = v_th + (q*n2D_min)/(Co)
    Vgs_max = v_th + (q*n2D_max)/(Co)

    # Calculate actual carrier concentration
    n2D = Co*(Vgs-v_th)/q

    # Calculate Rtot
    Rtot = rds_arbitrary(file_path,Vds=Vds,Vgs=Vgs)

    return n2D, Rtot


# Function to extract Rc, Rch, Rsh
# This function is a placeholder and needs to be implemented based on the specific resistance calculation method.
# Rtot at 4 different channel lengths, Rc extracted as the intercept on the y-axis
# Take the data from an external .csv file with Rtot at different channel lenghts
# 1) Rc = intercept on the y-axis at L=0
# 2) Rch = Rtot - 2Rc; 
# 3) Rsh = Rch / Lch
# Use small Vds (0.1V?)
def r_tlm(file_path):
    Rc = None
    Rch = None
    Rsh = None

    return  Rc, Rch, Rsh


# Function to extract the Channel Mobility from Id@Vg
# This function is a placeholder and needs to be implemented based on the specific mobility calculation method.
# ucon = 1/(q * ns * Rsh); ns = (Cin * Vov)/q (near the source; Rsh = sheet resistance extracted through TLM
# Rsh is extracted from the TLM
def mobility_con(file_path):
    dibl = None

    return dibl


# Store currents in csv file # MM
def compute(a=None):

    # Step 1: Input & output paths
    input_file_path = "id_vds.csv"
    output_file_path = "mosfet_parameters.csv"

    # Step 2: Compute parameters
    ion_value = ion(input_file_path)
    ioff_value = ioff(input_file_path)
    ion_off_ratio_value = ion_off_ratio(input_file_path)
    imax_value = imax(input_file_path)
    imin_value = imin(input_file_path)
    imm_ratio_value = imax_min_ratio(input_file_path)
    _, _, _, vth_ELR_value = Vth_ELR(input_file_path,Vds_bias = 1)
    vth_CC_value = Vth_CC(input_file_path,Vds_bias = 1)
    _, ss_value = SS(input_file_path)
    dibl_value = DIBL(input_file_path)
    n2D, Rtot = r_tot(input_file_path)

    # Step 3:  Store parameters in CSV file
    with open(output_file_path, "a", encoding="utf-8") as ofh:
        # Check if the file is empty or doesn't exist (MM)
        if os.stat(output_file_path).st_size == 0: #(MM)
            # Write the header row (MM)
            ofh.write("ion,ioff,iratio,imax,imin,imm_ratio,vth_ELR,vth_CC,ss,dibl,n2D,Rtot,res,ufe,mcon\n")
        # Write the data row
        ofh.write('%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s\n' % (ion_value,ioff_value,ion_off_ratio_value,imax_value,imin_value,imm_ratio_value,vth_ELR_value,vth_CC_value,ss_value,dibl_value,n2D,Rtot,None,None,None))
        # i += 1; 

    # pyexcel.merge_csv_to_a_book(glob.glob(output_file_path)) #, "id_vds.xlsx")
    # merge_all_to_a_book(glob.glob(output_file_path)) #, "id_vds.xlsx")


###
### Test the functions
###
# file_path = '/Users/macbookpro/Desktop/id_vds.csv'  # Replace with the path to your CSV file
# i_on = ion(file_path)
# i_off = ioff(file_path)
# on_off_ratio = ion_off_ratio(file_path)
# gm_peak, voltage_at_gm_peak, v_intersect, v_th = Vth_ELR(file_path)
# v_th = Vth_CC(file_path)
# slope_at_v_th, ss = SS(file_path)
# dibl = DIBL(file_path)
# n2D, r_tot = r_tot(file_path)
# uFE = mobility_fe(file_path)
# test = compute()


# if ioff:
#     current_at_0 = i_off
#     print(f"Ioff at Vgs = 0V: {current_at_0}")

# if ion:
#     current_at_1 = i_on
#     print(f"Ion at Vgs = 1V: {current_at_1}")

# if ion_off_ratio is not None:
#     print(f"I_on/I_off Ratio at Vds = 1V: {on_off_ratio}")

# if gm_peak:
#     # print(f"gm peak: {gm_peak}")
#     # print(f"Voltage at gm peak: {voltage_at_gm_peak}")
#     # print(f"Voltage intersect is: {v_intersect}")
#     print(f"Vth  is: {v_th}")

# if slope_at_v_th is not None:
#     print(f"SS is: {ss}")

# if uFE:
#     print(f"uFE is: {uFE}")

# if vth:
#     print(f"Vth is: {vth}")

# if vgs_min:
#     print(f"Vgs_min is: {vgs_min}")

# if vgs_max:
#     print(f"Vgs_max is: {vgs_max}")

# if n2D:
#     print(f"n2D is: {n2D:.2e}", "cm^-2") # cm^-2

# if r_tot:
#     print(f"Rtot is: {r_tot:.2e}", "kΩ*um") # kOhm * um

# if test:
#     test = StoreParameters_csv()
#     test

