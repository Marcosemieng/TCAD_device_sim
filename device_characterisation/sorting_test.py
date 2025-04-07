# Sorting test of files

import pandas as pd

def sort_id_vds_csv(file_path):
    """
    Sorts the data in the 'id_vds.csv' file.
    Specifically, for 'Id@V_gate_bias', it sorts:
    - First by Vds = 0.1, then by Vgs in ascending order.
    - Then by Vds = 1, then by Vgs in ascending order.

    Args:
        file_path (str): Path to the 'id_vds.csv' file.
    """
    try:
        # Load the CSV file into a pandas DataFrame
        df = pd.read_csv(file_path)
        print(f"CSV file '{file_path}' loaded successfully.")

        # Filter rows with Title = 'Id@V_gate_bias'
        df_gate_bias = df[df['Title'] == 'Id@V_gate_bias']
        # Sort the data for Vds = 0.1 by Vgs in ascending order
        df_vds_01 = df_gate_bias[df_gate_bias['Vds'] == 0.1].sort_values(by='Vgs')
        # Sort the data for Vds = 1 by Vgs in ascending order
        df_vds_1 = df_gate_bias[df_gate_bias['Vds'] == 1].sort_values(by='Vgs')
        # Combine the sorted data
        df_sorted_gate_bias = pd.concat([df_vds_01, df_vds_1])
        # Replace the original 'Id@V_gate_bias' rows with the sorted rows
        df_others = df[df['Title'] != 'Id@V_gate_bias']  # Keep rows that are not 'Id@V_gate_bias'
        df_sorted = pd.concat([df_others, df_sorted_gate_bias])
        # Save the sorted DataFrame back to the CSV file
        df_sorted.to_csv(file_path, index=False)
        print(f"Data sorted and saved back to '{file_path}'.")

        # Filter rows with Title = 'Id@V_drain_bias'
        df_drain_bias = df[df['Title'] == 'Id@V_drain_bias']
        # Sort the data for Vds = 0.1 by Vgs in ascending order
        df_vgs_01 = df_drain_bias[df_drain_bias['Vgs'] == 0.1].sort_values(by='Vds')
        # Sort the data for Vds = 1 by Vgs in ascending order
        df_vgs_07 = df_drain_bias[df_drain_bias['Vgs'] == 0.7].sort_values(by='Vds')
        # Sort the data for Vds = 1 by Vgs in ascending order
        df_vgs_1 = df_drain_bias[df_drain_bias['Vgs'] == 1].sort_values(by='Vds')
        # Combine the sorted data
        df_sorted_drain_bias = pd.concat([df_vgs_01, df_vgs_07, df_vgs_1])
        # Replace the original 'Id@V_gate_bias' rows with the sorted rows
        df_others = df[df['Title'] != 'Id@V_drain_bias']  # Keep rows that are not 'Id@V_drain_bias'
        df_sorted = pd.concat([df_others, df_sorted_gate_bias])
        # Save the sorted DataFrame back to the CSV file
        df_sorted.to_csv(file_path, index=False)
        print(f"Data sorted and saved back to '{file_path}'.")

    except FileNotFoundError:
        print(f"Error: File '{file_path}' not found.")
    except Exception as e:
        print(f"An error occurred: {e}")


# Example usage
file_path = "id_vds.csv"  # Replace with the actual path to your CSV file
sort_id_vds_csv(file_path)