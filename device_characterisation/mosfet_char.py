import csv
import numpy as np

# Function to extract Ion (Vg=Vd) from Id@Vg at Vds=Vdd=1V
def mosfet_ion_char(file_path):
    Vds_bias = 1  # Vds=1V bias value to filter the data: data must be extracted at this Vds=Vdd=1V
    voltages = []
    currents = []

    # Open the CSV file and read the data
    with open(file_path, mode='r', encoding='utf-8') as csv_file:
        reader = csv.DictReader(csv_file)  # Use DictReader to access columns by name
        for row in reader:
            try:
                # Process only rows where Vds == Vds_bias
                if float(row['Vds']) == Vds_bias:
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
def mosfet_ioff_char(file_path):
    Vds_bias = 1  # Vds=1V bias value to filter the data: data must be extracted at this Vds=Vdd=1V
    voltages = []
    currents = []

    # Open the CSV file and read the data
    with open(file_path, mode='r', encoding='utf-8') as csv_file:
        reader = csv.DictReader(csv_file)  # Use DictReader to access columns by name
        for row in reader:
            try:
                # Process only rows where Vds == Vds_bias
                if float(row['Vds']) == Vds_bias:
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
def mosfet_on_off_ratio_char(file_path):
    # Get the I_on and I_off values
    i_on = mosfet_ion_char(file_path)
    i_off = mosfet_ioff_char(file_path)

    # Ensure both values are valid
    if i_on is None or i_off is None or i_off == 0:
        print("Error: Invalid I_on or I_off values.")
        return None

    # Calculate the ratio
    on_off_ratio = i_on / i_off
    return on_off_ratio


# Function to extract the threshold voltage Vth from Id@Vg at Vds=Vdd=1V, by ELR method
def mosfet_Vth_char(file_path):
    Vds_bias = 1  # Vds=1V bias value to filter the data: data must be extracted at this Vds=Vdd=1V
    voltages = []
    currents = []

    # Open the CSV file and read the data
    with open(file_path, mode='r', encoding='utf-8') as csv_file:
        reader = csv.DictReader(csv_file)  # Use DictReader to access columns by name
        for row in reader:
            try:
                # Process only rows where Vds == Vds_bias
                if float(row['Vds']) == Vds_bias:
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

    # Find Vth
    v_th = v_intersect - (Vds_bias/2)

    return gm_peak, voltage_at_gm_peak, v_intersect, v_th


def mosfet_SS_char(file_path):
    # Call mosfet_Vth_char to get v_th
    _, _, _, v_th = mosfet_Vth_char(file_path)

    if v_th is None:
        print("Error: Unable to calculate Vth.")
        return None

    # Extract voltages and currents from the CSV file
    Vds_bias = 1  # Vds=1V bias value to filter the data
    voltages = []
    currents = []

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



# Test the functions
file_path = '/Users/macbookpro/Desktop/id_vds.csv'  # Replace with the path to your CSV file
i_on = mosfet_ion_char(file_path)
i_off = mosfet_ioff_char(file_path)
on_off_ratio = mosfet_on_off_ratio_char(file_path)
gm_peak, voltage_at_gm_peak, v_intersect, v_th = mosfet_Vth_char(file_path)
slope_at_v_th, ss = mosfet_SS_char(file_path)

if i_off:
    current_at_0 = i_off
    print(f"Ioff at Vgs = 0V: {current_at_0}")

if i_on:
    current_at_1 = i_on
    print(f"Ion at Vgs = 1V: {current_at_1}")

if on_off_ratio is not None:
    print(f"I_on/I_off Ratio at Vds = 1V: {on_off_ratio}")

if gm_peak:
    # print(f"gm peak: {gm_peak}")
    # print(f"Voltage at gm peak: {voltage_at_gm_peak}")
    # print(f"Voltage intersect is: {v_intersect}")
    print(f"Vth  is: {v_th}")

if slope_at_v_th is not None:
    print(f"SS is: {ss}")
