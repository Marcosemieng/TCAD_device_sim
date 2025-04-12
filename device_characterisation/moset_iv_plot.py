import pandas as pd
import matplotlib.pyplot as plt
# import scienceplots  # Ensure this is installed if you're using the 'science' style

# Use the 'science' style for the plot
# plt.style.use('science')

# Plot I@Vds
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

# Plot I@Vgs
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


# Test
print_IVgs = print_IVgs()
print_IVds = print_IVds()