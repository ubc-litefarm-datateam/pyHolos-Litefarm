import os
import sys
import json
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

# Generate comparisons
def generate_comparison(crop_name):

    from plotting_functions import get_holos_results, get_pyholos_data
        
    base_dir = os.path.join(os.path.dirname(__file__), '..', '..')
    df_holos = pd.read_csv(os.path.join(base_dir, 'data/outputs/result_comparison/holos_outputs.csv'))
    df_py = pd.read_csv(os.path.join(base_dir, 'data/outputs/result_comparison/python_holos.csv'))
    
    holos_data = get_holos_results(df_holos, crop_name)
    holos_data.insert(0, 'Source', 'Holos Software')
    
    py_data = get_pyholos_data(df_py, crop_name)
    py_data.insert(0, 'Source', 'PyHolos')
    
    comparison = pd.concat([holos_data, py_data], ignore_index=True)
    comparison = comparison.round(2)
    
    return comparison

# Define main functions to be called externally
def get_potato_comparison():
    return generate_comparison('Potatoes')

def get_soybean_comparison():
    return generate_comparison('Soybeans')

def plot_comparisons(potato_comparison, soybean_comparison):
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(9, 3))
    markers = {'Holos Software': 's', 'PyHolos': '^'}  # Square and triangle markers
    colors = {'Holos Software': 'blue', 'PyHolos': 'red'}  # Define colors

    # Plotting for potatoes
    for key, grp in potato_comparison.groupby(['Source']):
        key = key[0] if isinstance(key, tuple) else key
        ax1.scatter(grp['Yield'], grp['N2O Direct CO2e'], label=key, marker=markers[key], color=colors[key], s=100)
    ax1.set_title('Potatoes')
    ax1.set_xlabel('Yield (kg/ha)')
    ax1.set_ylabel("N2O Emission (kg CO2e)")
    ax1.legend()
    ax1.set_ylim(bottom=0)
    x_ticks_potatoes = np.linspace(potato_comparison['Yield'].min(), potato_comparison['Yield'].max(), 5)
    ax1.set_xticks(ticks=x_ticks_potatoes, labels=[f"{(x/10000)}" for x in x_ticks_potatoes])
    ax1.grid(True)

    # Plotting for soybeans
    for key, grp in soybean_comparison.groupby(['Source']):
        key = key[0] if isinstance(key, tuple) else key
        ax2.scatter(grp['Yield'], grp['N2O Direct CO2e'], label=key, marker=markers[key], color=colors[key], s=100)
    ax2.set_title('Soybeans')
    ax2.set_xlabel('Yield (kg/ha)')
    ax2.set_ylabel("N2O Emission (kg CO2e)")
    ax2.legend()
    ax2.set_ylim(bottom=0)
    x_ticks_soybeans = np.linspace(soybean_comparison['Yield'].min(), soybean_comparison['Yield'].max(), 5)
    ax2.set_xticks(ticks=x_ticks_soybeans, labels=[f"{(x/10000)}" for x in x_ticks_soybeans])
    ax2.grid(True)

    plt.tight_layout()
    plt.show()

def main():
    # Test the get_potato_comparison function
    try:
        potato_comparison = get_potato_comparison()
        print("Potato Comparison Data:")
        print(potato_comparison.head())  # Display the first few rows of the dataframe
    except Exception as e:
        print(f"Error in getting potato comparison: {str(e)}")

    # Test the get_soybean_comparison function
    try:
        soybean_comparison = get_soybean_comparison()
        print("\nSoybean Comparison Data:")
        print(soybean_comparison.head())  # Display the first few rows of the dataframe
    except Exception as e:
        print(f"Error in getting soybean comparison: {str(e)}")

if __name__ == "__main__":
    main()
