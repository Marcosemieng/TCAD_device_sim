# This module produces plots of mosfet parameters measured by TLM
# The file can be selected externally. 
# The file with the parameters must be already available (can be produced by the 'mosfet_TLM_characterisation' module)

import os
import csv
import pandas as pd
import numpy as np

from scipy.stats import linregress
import matplotlib.pyplot as plt

from tkinter import Tk
from tkinter.filedialog import askopenfilenames, asksaveasfilename

import devsim.python_packages.simple_physics as simple_physics


# Function to merge CSV files
# TO-DO: give automatically the channel length (to be added at priori during the simulation)
def open_csv(input=None):
    """
    Allows the user to select 4 different .csv files via a GUI and merges their content into a single .csv file.
    Adds a new column "Lch" to the output file.
    """
    # Step 1: Open a file selection dialog to select 4 .csv files
    Tk().withdraw()  # Hide the root Tkinter window
    print("Please select 4 .csv files to merge.")
    file_paths = askopenfilenames(
        title="Select a file containing TLM parameters",
        filetypes=[("CSV Files", "*.csv")],
        multiple=True
    )

    # Ensure exactly 3 files are selected
    if len(file_paths) != 1:
        print("Error: You must select 1 .csv file.")
        return

    if not file_paths:
        print("Error: No input file specified.")
        return

    return file_paths


# Function to plot the columns of a CSV file
def plot_tlm_parameters(input=None):
    """
    Reads a .csv file and generates a mosaic of plots for each column using matplotlib.
    The x-axis values are taken from the 'Lch' column in the .csv file.
    Columns with 'None' or NaN values are excluded from the plots.

    Args:
        file_path (str): Path to the .csv file.
    """
    try:
        # Step 0: Select .csv file
        file_path = open_csv()

        # Step 1: Read the .csv file into a pandas DataFrame
        data = pd.read_csv(file_path[0])  # Use the first file from the selection

        # Ensure the 'Lch' column exists
        if 'Lch' not in data.columns:
            print("Error: The 'Lch' column is missing from the .csv file.")
            return

        # Step 2: Exclude columns with 'None' or NaN values
        valid_columns = [col for col in data.columns if col != 'Lch' and not data[col].isnull().any()]

        if not valid_columns:
            print("Error: No valid columns to plot (all columns contain 'None' or NaN values).")
            return

        # Step 3: Generate a mosaic of plots for valid columns
        num_columns = len(valid_columns)
        num_rows = (num_columns + 2) // 3  # Arrange plots in a grid with 3 columns per row

        fig, axes = plt.subplots(num_rows, 3, figsize=(15, 5 * num_rows))  # Create subplots
        axes = axes.flatten()  # Flatten the axes array for easy iteration

        for i, column in enumerate(valid_columns):
            ax = axes[i]  # Get the corresponding subplot
            ax.plot(data['Lch'], data[column], marker='o', label=column)  # Use 'Lch' as the x-axis
            ax.set_title(f"{column} vs Lch")  # Set the title
            ax.set_xlabel("Lch (nm)")  # X-axis represents 'Lch'
            ax.set_ylabel(column)  # Y-axis represents the column values
            ax.legend()  # Add a legend
            ax.grid(True)  # Add a grid

        # Hide any unused subplots
        for j in range(i + 1, len(axes)):
            fig.delaxes(axes[j])

        plt.tight_layout()  # Adjust layout to avoid overlapping

        # Step 4: Save the plot in the same location as the input .csv file
        output_file = os.path.splitext(file_path[0])[0] + "_plots.png"  # Replace .csv with _plots.png
        plt.savefig(output_file, dpi=300)  # Save the figure with high resolution
        print(f"Plot saved to: {output_file}")

        # Step 5: Show the plot
        plt.show()  # Display the mosaic of plots

    except FileNotFoundError:
        print(f"Error: File '{file_path}' not found.")
    except Exception as e:
        print(f"An error occurred: {e}")


# Function to produce all the plots needed
def compute(input=None):

    # Step 1: Select input files and generate merged file
    file_path = open_csv()

    # Step 2: Produce plots
    # Text here


###
### Test the functions
###

# Example usage
# input_file = open_csv()
# if input_file: 
#     print(f"Selected file: {input_file[0]}")

# Example usage
plot_tlm_parameters()