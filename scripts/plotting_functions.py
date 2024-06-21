import json
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd


def plot_boxplot(data_raw):
    input_data = data_raw['Input Parameters']
    input_data_flattened = {}

    for outer_key, inner_dict in input_data.items():
        for inner_key, value in inner_dict.items():
            input_data_flattened[inner_key] = value

    emission_data = data_raw['Total Direct Nitrogen Emission']
    baseline = emission_data['P']['co2_crop_direct'][0]
    value_list = [key for key, value in input_data_flattened.items() if len(value) > 1]
    remove_list = ['locations']
    value_list = [x for x in value_list if x not in remove_list]

    variable_list = ['P', 'PE', 'soil_texture', 'RF_AM', 'RF_NS', 'S_r', 'moisture', 'R_p']
    v_list = ['P', 'PE', 'SOIL_TX', 'RF_AM', 'RF_NS', 'S_r', 'Moisture', 'R_p']
    data_boxplot = [np.array(emission_data[key]['co2_crop_direct']) for key in variable_list]
    filtered_data_boxplot = [data[~np.isnan(data)] for data in data_boxplot]

    plt.figure(figsize=(13, 6))
    plt.boxplot(filtered_data_boxplot, labels=v_list)
    plt.ylabel(r'N$_2$O Direct Emission CO$_2$e', fontsize=21)
    plt.title(r'N$_2$O Direct Emissions (CO$_2$e) Across Different Input Parameters', fontsize=23)
    plt.axhline(y=baseline, color='blue', linestyle='--', linewidth=1, label='Farmer mode reference')

    # Add vertical line to separate external and user-defined parameters
    plt.axvline(x=3.5, color='gray', linestyle='-.', linewidth=1)
    plt.text(2, 1.1*plt.ylim()[0] - (plt.ylim()[1] /1000), 'External Database', horizontalalignment='center', fontsize=15, color='grey')
    plt.text(6, 1.1*plt.ylim()[0] - (plt.ylim()[1] /1000), 'User Defined Distribution', horizontalalignment='center', fontsize=15, color='grey')
    plt.tick_params(axis='both', labelsize=19)
    plt.legend(fontsize=15)
    plt.show()



def plot_by_eco_id(df, variables):
    for crop_type in df['crop_type'].unique():
        fig, axs = plt.subplots(1, 3, figsize=(20,20), sharey=False)
        for i, var in enumerate(variables):
            ax = axs[i]
            
            data = df[(df['crop_type'] == crop_type) & (df['variable'] == var) & (~df['emission_value'].isna())].copy()
            
            
            min_vals = data.groupby('eco_id')['param_value'].min()
            max_vals = data.groupby('eco_id')['param_value'].max()
            range_vals = max_vals - min_vals
            

            ordered_eco_ids = range_vals.sort_values().index
            data['eco_id'] = pd.Categorical(data['eco_id'], categories=ordered_eco_ids, ordered=True)
            data = data.sort_values(by='eco_id')
            
            eco_ids = data['eco_id'].unique()
            emission_values = [data[data['eco_id'] == eco_id]['emission_value'].values for eco_id in eco_ids]

            ax.boxplot(emission_values, vert=False, labels=eco_ids)
        
            y_labels = [f'{eco_id}\n({min_vals[eco_id]:.1f}-{max_vals[eco_id]:.1f})' for eco_id in eco_ids]
            
            ax.set_title(f'{crop_type} N2O Direct Emission - {var}', fontsize=22)
            ax.set_xlabel(r'N$_2$O Direct Emission (CO2e)', fontsize=18)
            if i == 0:
                ax.set_ylabel('ECO ID', fontsize=18)
            ax.set_yticks(np.arange(1, len(eco_ids) + 1))
            ax.set_yticklabels(y_labels, fontsize=12)
            ax.tick_params(axis='x', labelsize=12)
            
        plt.tight_layout()
        plt.show()


def plot_by_crop(df, variables):
    def add_emission_annotations(ax, data, positions):
        grouped = data.groupby(['crop_type'])['emission_value']
        for pos, (crop, group) in zip(positions, grouped):
            min_val = group.min()
            max_val = group.max()
            q1_val = group.quantile(0.25)
            median_val = group.median()
            q3_val = group.quantile(0.75)

            ax.annotate(f'Q1:{q1_val:.1f}', xy=(pos, q1_val), xytext=(pos - 0.35, q1_val),
                        fontsize=12, color='purple', ha='center')
            ax.annotate(f'Q3:{q3_val:.1f}', xy=(pos, q3_val), xytext=(pos - 0.35, q3_val),
                        fontsize=12, color='purple', ha='center')
            ax.annotate(f'{median_val:.1f}', xy=(pos, median_val), xytext=(pos + 0.35, median_val + 2),
                        fontsize=12, color='purple', ha='right')

    def variable_width_boxplot(ax, data, var, positions):
        widths = []
        labels = []
        for crop in data['crop_type'].unique():
            crop_data = data[data['crop_type'] == crop]
            param_values = crop_data['param_value']
            param_range = param_values.max() - param_values.min()
            widths.append(param_range)

            min_val = param_values.min()
            max_val = param_values.max()
            labels.append(f'{crop}\n({min_val:.1f} - {max_val:.1f})')

        total_width = sum(widths)
        widths = [width / total_width for width in widths]  # Normalize widths

        box_data = [data[data['crop_type'] == crop]['emission_value'].dropna() for crop in data['crop_type'].unique()]
        boxplot = ax.boxplot(box_data, positions=positions, widths=widths, patch_artist=True)
        
        for patch, width in zip(boxplot['boxes'], widths):
            patch.set_facecolor('white')
            patch.set_edgecolor('black')

        ax.set_xticklabels(labels, fontsize=20, rotation=0)

        return widths
    provinces = df['province'].unique()
    for province in provinces:
        fig, axs = plt.subplots(1, len(variables), figsize=(30, 8), sharey=False)
        for i, var in enumerate(variables):
            ax = axs[i]
            data = df[(df['province'] == province) & (df['variable'] == var)]
            crop_types = data['crop_type'].unique()
            positions = np.arange(1, len(crop_types) + 1)
            
            widths = variable_width_boxplot(ax, data, 'emission_value', positions)
            add_emission_annotations(ax, data, positions)
            
            ax.set_title(f'{province} - {var}', fontsize=25)
            ax.set_ylabel(f'N2O Direct Emission ({var})', fontsize=20)
            ax.set_xticks(positions)
        
        plt.suptitle(f'{province} - Emissions by Crop Type', fontsize=30)
        plt.tight_layout(rect=[0, 0, 1, 0.95])
        plt.show()





def plot_by_province(df, variables):
    def add_emission_annotations(ax, data, positions):
        grouped = data.groupby(['province'], observed=True)['emission_value']
        for pos, (province, group) in zip(positions, grouped):
            min_val = group.min()
            max_val = group.max()
            q1_val = group.quantile(0.25)
            median_val = group.median()
            q3_val = group.quantile(0.75)

            if min_val > 100:
                min_xytext = (min_val - 50, pos)
            else:
                min_xytext = (min_val - 20, pos)

            ax.annotate(f'Q1:{q1_val:.1f}', xy=(q1_val, pos), xytext=(q1_val, pos - 0.4),
                        fontsize=9, color='purple', ha='center')
            ax.annotate(f'Q3:{q3_val:.1f}', xy=(q3_val, pos), xytext=(q3_val, pos + 0.3),
                        fontsize=9, color='purple', ha='center')

    def boxplot_by_province(ax, data, var, positions):
        box_data = [data[data['province'] == province]['emission_value'].dropna() for province in data['province'].cat.categories]
        boxplot = ax.boxplot(box_data, positions=positions, patch_artist=True, vert=False, labels=data['province'].cat.categories)

        for patch in boxplot['boxes']:
            patch.set_facecolor('white')
            patch.set_edgecolor('black')

    crops = df['crop_type'].unique()
    for crop in crops:
        fig, axs = plt.subplots(1, len(variables), figsize=(30, 10), sharex=False)
        for i, var in enumerate(variables):
            ax = axs[i]
            data = df[(df['crop_type'] == crop) & (df['variable'] == var)].copy()

            min_vals = data.groupby('province', observed=True)['param_value'].min()
            max_vals = data.groupby('province', observed=True)['param_value'].max()
            range_vals = max_vals - min_vals
            
            ordered_provinces = range_vals.sort_values(ascending=True).index.tolist()
            data['province'] = pd.Categorical(data['province'], categories=ordered_provinces, ordered=True)
            data = data.sort_values('province')
            
            provinces = data['province'].cat.categories
            positions = np.arange(1, len(provinces) + 1)
            
            boxplot_by_province(ax, data, 'emission_value', positions)
            add_emission_annotations(ax, data, positions)
            
            province_labels = [f'{province}\n({min_vals[province]:.1f} - {max_vals[province]:.1f})' for province in provinces]
            
            ax.set_title(f'{crop} - {var}', fontsize=16)
            ax.set_xlabel(f'N2O Direct Emission ({var})', fontsize=14)
            ax.set_yticks(positions)
            ax.set_yticklabels(province_labels, fontsize=12)
            
        plt.suptitle(f'{crop} - Emissions by Province', fontsize=20)
        plt.tight_layout(rect=[0, 0, 1, 0.95])
        plt.show()



def get_holos_results(df, crop_name):
    columns = ['Farm',
               'Field',
               'Time period',
               'Year',
               'Crop',
               'Yield (kg ha^-1)',
               'Moisture content (%)',
               'Harvest method',
               'Tillage type',
               'Product returned to soil (%)',
               'Straw returned to soil (%)',
               'Roots returned to soil (%)',
               'Relative C allocation coefficient of product',
               'Relative C allocation coefficient of straw',
               'Relative C allocation coefficient of roots',
               'Relative C allocation coefficient of extraroots',
               'Plant Carbon in Product (C_p) (kg C ha^-1)',
               'Carbon input from product (C_ptoSoil) (kg C ha^-1)',
               'Carbon input from straw (C_s) (kg C ha^-1)',
               'Carbon input from roots (C_r) (kg C ha^-1)',
               'Carbon input from extraroots (C_e) (kg C ha^-1)',
               'Above Ground Carbon Input (i_ag) (kg C ha^-1)',
               'Below Ground Carbon Input (i_bg) (kg C ha^-1)',
               'N2O-N From Crop Residues (N2O-N_CRNdirect) (kg N2O-N field^-1)',
               'Direct_N2O_(kg_CO2e)']
    
    selected_data = df[columns]
    column_rename_mapping = {
        'Farm': 'Farm',
        'Field': 'Field',
        'Time period': 'Period',
        'Year': 'Year',
        'Crop': 'Crop',
        'Yield (kg ha^-1)': 'Yield',
        'Moisture content (%)': 'Moisture',
        'Harvest method': 'Harvest',
        'Tillage type': 'Tillage',
        'Product returned to soil (%)': 'S_p',
        'Straw returned to soil (%)': 'S_s',
        'Roots returned to soil (%)': 'S_r',
        'Relative C allocation coefficient of product': 'R_p',
        'Relative C allocation coefficient of straw': 'R_s',
        'Relative C allocation coefficient of roots': 'R_r',
        'Relative C allocation coefficient of extraroots': 'R_e',
        'Plant Carbon in Product (C_p) (kg C ha^-1)': 'C_p',
        'Carbon input from product (C_ptoSoil) (kg C ha^-1)': 'C_p_to_soil',
        'Carbon input from straw (C_s) (kg C ha^-1)': 'C_s',
        'Carbon input from roots (C_r) (kg C ha^-1)': 'C_r',
        'Carbon input from extraroots (C_e) (kg C ha^-1)': 'C_e',
        'Above Ground Carbon Input (i_ag) (kg C ha^-1)': 'Aboveground Carbon Input',
        'Below Ground Carbon Input (i_bg) (kg C ha^-1)': 'Belowground Carbon Input',
        'N2O-N From Crop Residues (N2O-N_CRNdirect) (kg N2O-N field^-1)': 'N2O-N From Crop Residues',
        'Direct_N2O_(kg_CO2e)': 'N2O Direct CO2e'
    }
    
    renamed_data = selected_data.rename(columns=column_rename_mapping)
    
    selected_columns = ['Crop',
                        'Yield',
                        'Aboveground Carbon Input',
                        'Belowground Carbon Input',
                        'N2O-N From Crop Residues',
                        'N2O Direct CO2e']
    
    filtered_data = renamed_data[selected_columns]
    crop_data = filtered_data[filtered_data['Crop'] == crop_name].sort_values(by='Yield').reset_index(drop=True)
    
    if crop_data.empty:
        print(f"No data found for crop: {crop_name}")
        return
    
    return crop_data

def get_pyholos_data(df, crop_name):
    columns = [
        'crop',
        'yield',
        'above_ground_carbon_input',
        'below_ground_carbon_input',
        'n_crop_direct',
        'co2_crop_direct'
    ]

    selected_data = df[columns]
    column_rename_mapping = {
        'crop': 'Crop',
        'yield': 'Yield',
        'above_ground_carbon_input': 'Aboveground Carbon Input',
        'below_ground_carbon_input': 'Belowground Carbon Input',
        'n_crop_direct': 'N2O-N From Crop Residues',
        'co2_crop_direct': 'N2O Direct CO2e'
    }

    renamed_data = selected_data.rename(columns=column_rename_mapping)

    filtered_data = renamed_data[renamed_data['Crop'] == crop_name]

    if filtered_data.empty:
        print(f"No data found for crop: {crop_name}")
        return

    sorted_data = filtered_data.sort_values(by='Yield').reset_index(drop=True)
    return sorted_data
