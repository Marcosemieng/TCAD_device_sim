import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.ticker import ScalarFormatter
from tkinter import Tk, filedialog
# import scienceplots  # Ensure this is installed if you're using the 'science' style

# Use the 'science' style for the plot
# plt.style.use('science')

# Plot I@Vds from file within VS
def print_IVds():

    csv_file_path = "id_vds.csv"  # Replace with the actual path to your CSV file
    try:
        df = pd.read_csv(csv_file_path)
        print(f"CSV file '{csv_file_path}' loaded successfully.")
    except FileNotFoundError:
        print(f"Error: CSV file '{csv_file_path}' not found.")
        exit()

    # Filter the data for 'Id@V_drain_bias' and specific Vds values
    df_drain_bias = df[df['Title'] == 'Id@V_drain_bias']  # Filter rows with Title = 'Id@V_drain_bias'
    df_vds_01 = df_drain_bias[df_drain_bias['Vgs'] == 0.1]  # Filter rows with Vds = 0.1
    df_vds_07 = df_drain_bias[df_drain_bias['Vgs'] == 0.7]  # Filter rows with Vds = 0.7
    df_vds_1 = df_drain_bias[df_drain_bias['Vgs'] == 1]  # Filter rows with Vds = 1

    # Plot the data
    plt.figure(figsize=(8, 6))  # Set the figure size

    # Plot for Vgs = 0.1
    plt.plot(df_vds_01['Vds'], df_vds_01['Ids'], marker='o', label='Vgs = 0.1')

    # Plot for Vgs = 0.5
    plt.plot(df_vds_07['Vds'], df_vds_07['Ids'], marker='o', label='Vgs = 0.7')

    # Plot for Vgs = 1
    plt.plot(df_vds_1['Vds'], df_vds_1['Ids'], marker='s', label='Vgs = 1')

    # Customize the plot
    plt.xlabel('Vds (Drain Voltage) [V]')  # X-axis label
    plt.ylabel('Ids (Drain Current) [A/cm]')  # Y-axis label
    # plt.yscale('log')  # Set the y-axis to logarithmic scale
    plt.title('Ids vs Vds for Different Vgs')  # Plot title
    plt.legend()  # Add a legend
    plt.grid(True)  # Add a grid
    plt.tight_layout()  # Adjust layout to avoid clipping

    # Show the plot
    plt.show()


# Plot I@Vgs from file within VS
def print_IVgs():

    csv_file_path = "id_vds.csv"  # Replace with the actual path to your CSV file
    try:
        df = pd.read_csv(csv_file_path)
        print(f"CSV file '{csv_file_path}' loaded successfully.")
    except FileNotFoundError:
        print(f"Error: CSV file '{csv_file_path}' not found.")
        exit()

    # Filter the data for 'Id@V_drain_bias' and specific Vds values
    df_gate_bias = df[df['Title'] == 'Id@V_gate_bias']  # Filter rows with Title = 'Id@V_drain_bias'
    df_vgs_01 = df_gate_bias[df_gate_bias['Vds'] == 0.1]  # Filter rows with Vds = 0.1
    df_vgs_1 = df_gate_bias[df_gate_bias['Vds'] == 1]  # Filter rows with Vds = 1

    # Plot the data
    plt.figure(figsize=(8, 6))  # Set the figure size

    # Plot for Vds = 0.1
    plt.plot(df_vgs_01['Vgs'], df_vgs_01['Ids'], marker='o', label='Vds = 0.1')

    # Plot for Vds = 1
    plt.plot(df_vgs_1['Vgs'], df_vgs_1['Ids'], marker='s', label='Vds = 1')

    # Customize the plot
    plt.xlabel('Vgs (Gate Voltage) [V]')  # X-axis label
    plt.ylabel('Ids (Drain Current) [A/cm]')  # Y-axis label
    plt.yscale('log')  # Set the y-axis to logarithmic scale
    plt.title('Ids vs Vgs for Different Vds')  # Plot title
    plt.legend()  # Add a legend
    plt.grid(True)  # Add a grid
    plt.tight_layout()  # Adjust layout to avoid clipping

    # Show the plot
    plt.show()


# Plot I@Vds from an external selectable file
# This is a placeholder function
def print_IVds_ext():
    plot = None

    return plot


# Plot I@Vgs from an external selectable file
# This is a placeholder function
def print_IVgs_ext():
    plot = None

    return plot


# Plot multiple I@Vds from an external selectable file (at a fixed Vgs = 1V)
# TO-DO: move this function into "4_mosfet_TLM_plot.py"
def print_IVds_multiple_ext(Vgs_select=1):
    """
    Allows the user to select one or multiple .csv files via a pop-up window
    and plots the Ids vs Vds curves from the selected files on the same graph.
    The y-axis values (Ids) can be scaled by a desired factor.
    """
    # Step 1: Open a file selection dialog to select one or multiple .csv files
    Tk().withdraw()  # Hide the root Tkinter window
    file_paths = filedialog.askopenfilenames(
        title="Select one or multiple CSV files",
        filetypes=[("CSV Files", "*.csv")]
    )

    if not file_paths:
        print("No files selected.")
        return

    # Step 2: Prompt the user for a scaling factor for the y-axis
    try:
        scaling_factor = float(input("Enter the scaling factor for the y-axis (Ids): "))
    except ValueError:
        print("Invalid scaling factor. Using default value of 1.")
        scaling_factor = 1.0

    # Step 3: Initialize the plot
    plt.figure(figsize=(8, 6))  # Set the figure size

    # Step 4: Loop through each selected file and plot the data
    for file_path in file_paths:
        try:
            # Load the CSV file into a DataFrame
            df = pd.read_csv(file_path)
            print(f"CSV file '{file_path}' loaded successfully.")

            # Filter the data for 'Id@V_drain_bias'
            df_drain_bias = df[df['Title'] == 'Id@V_drain_bias']

            # Plot the data for only the selected Vgs value
            df_vgs = df_drain_bias[df_drain_bias['Vgs'] == Vgs_select]
            plt.plot(
                df_vgs['Vds'], df_vgs['Ids'] * scaling_factor, marker='o',
                label=f"{file_path.split('/')[-1]}: Vgs = {Vgs_select}"
            )

        except FileNotFoundError:
            print(f"Error: CSV file '{file_path}' not found.")
        except Exception as e:
            print(f"An error occurred while processing '{file_path}': {e}")

    # Step 5: Customize the plot
    plt.xlabel('Vds [V]')  # X-axis label
    # TO-DO: make this automatic every time scaling factor is = 1
    plt.ylabel(f'Ids [A/cm]')  # Y-axis label (as is: A/cm)
    # plt.ylabel(f'Ids [uA/um]')  # Y-axis label (scaled by 1e-2)
    plt.title('Ids@Vds vs. Lch')  # Plot title
    plt.legend()  # Add a legend
    # plt.grid(True)  # Add a grid
    plt.tight_layout()  # Adjust layout to avoid clipping

    # Step 6: Set the y-axis to scientific notation
    ax = plt.gca()  # Get the current axis
    ax.yaxis.set_major_formatter(ScalarFormatter(useMathText=True))
    ax.yaxis.get_major_formatter().set_scientific(True)
    ax.yaxis.get_major_formatter().set_powerlimits((-1, 1))  # Adjust the range for scientific notation

    plt.tight_layout()  # Adjust layout to avoid clipping

    # Step 7: Show the plot
    plt.show()


# Plot multiple I@Vgs from an external selectable file (at a fixed Vds = 1V)
# TO-DO: move this function into "4_mosfet_TLM_plot.py"
def print_IVgs_multiple_ext(Vds_select=1):
    """
    Allows the user to select one or multiple .csv files via a pop-up window
    and plots the Ids vs Vds curves from the selected files on the same graph.
    """
    # Step 1: Open a file selection dialog to select one or multiple .csv files
    Tk().withdraw()  # Hide the root Tkinter window
    file_paths = filedialog.askopenfilenames(
        title="Select one or multiple CSV files",
        filetypes=[("CSV Files", "*.csv")]
    )

    if not file_paths:
        print("No files selected.")
        return
    
    # Step 2: Prompt the user for a scaling factor for the y-axis
    try:
        scaling_factor = float(input("Enter the scaling factor for the y-axis (Ids): "))
    except ValueError:
        print("Invalid scaling factor. Using default value of 1.")
        scaling_factor = 1.0

    # Step 3: Initialize the plot
    plt.figure(figsize=(8, 6))  # Set the figure size

    # Step 4: Loop through each selected file and plot the data
    for file_path in file_paths:
        try:
            # Load the CSV file into a DataFrame
            df = pd.read_csv(file_path)
            print(f"CSV file '{file_path}' loaded successfully.")

            # Filter the data for 'Id@V_gate_bias'
            df_gate_bias = df[df['Title'] == 'Id@V_gate_bias']

            # Plot the data for only a Vgs value

            df_vds = df_gate_bias[df_gate_bias['Vds'] == Vds_select]
            plt.plot(
                df_vds['Vgs'], df_vds['Ids'] * scaling_factor, marker='o',
                label=f"{file_path.split('/')[-1]}: Vds = {Vds_select}"
            )

            # Plot the data for each unique Vgs value
            # for vgs_value in df_drain_bias['Vgs'].unique():
            #     df_vgs = df_drain_bias[df_drain_bias['Vgs'] == vgs_value]
            #     plt.plot(
            #         df_vgs['Vds'], df_vgs['Ids'], marker='o',
            #         label=f"{file_path.split('/')[-1]}: Vgs = {vgs_value}"
            #     )

        except FileNotFoundError:
            print(f"Error: CSV file '{file_path}' not found.")
        except Exception as e:
            print(f"An error occurred while processing '{file_path}': {e}")

    # Step 5: Customize the plot
    plt.xlabel('Vgs [V]')  # X-axis label
    # TO-DO: make this automatic every time scaling factor is = 1
    plt.ylabel('Ids [A/cm]')  # Y-axis label (no scaling factor = 1)
    # plt.ylabel(f'Ids [uA/um]')  # Y-axis label (scaled by 1e2 = 100)
    plt.yscale('log')  # Set the y-axis to logarithmic scale
    plt.title('Ids#Vgs vs. Lch')  # Plot title
    plt.legend()  # Add a legend
    plt.grid(False)  # Add a grid
    plt.tight_layout()  # Adjust layout to avoid clipping

    # Step 6: Set the y-axis to scientific notation
    # ax = plt.gca()  # Get the current axis
    # ax.yaxis.set_major_formatter(ScalarFormatter(useMathText=True))
    # ax.yaxis.get_major_formatter().set_scientific(True)
    # ax.yaxis.get_major_formatter().set_powerlimits((-1, 1))  # Adjust the range for scientific notation

    # Step 7: Show the plot
    plt.show()


# Test
# print_IVgs = print_IVgs()
# print_IVds = print_IVds()
print_IVgs_multiple_ext()
# print_IVds_multiple_ext()