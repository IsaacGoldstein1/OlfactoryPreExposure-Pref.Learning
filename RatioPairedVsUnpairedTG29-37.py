import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

# Load the Excel file
file_path = '/Users/isaac/Downloads/Unsurgerized Data (TG29-37) (1).xlsx'  # Modify with the actual path to your Excel file

# Function to calculate the ratio of paired to unpaired licks
def calculate_lick_ratios(sheet_name):
    data = pd.read_excel(file_path, sheet_name=sheet_name)
    paired = data[data['SOLUTION'] == 'P']['LICKS'].sum()
    unpaired = data[data['SOLUTION'] == 'U']['LICKS'].sum()
    return paired / unpaired if unpaired != 0 else float('nan')  # Avoid division by zero

# Create a dictionary to store the ratio data for each animal
ratios = {}
sheets = pd.ExcelFile(file_path).sheet_names

# Iterate through sheets to calculate the ratios
for sheet in sheets:
    animal_id = sheet.split(' ')[1]
    condition = sheet.split(' ')[3]
    ratios.setdefault(animal_id, {})[condition.lower()] = calculate_lick_ratios(sheet)

# Prepare data for plotting by grouping
group1 = {k: v for k, v in ratios.items() if int(k) in range(29, 33)}
group2 = {k: v for k, v in ratios.items() if int(k) in range(33, 38)}

def plot_aggregated_group(group, title):
    labels = ['Pre', 'Post']
    pre_values = [group[animal]['pre'] for animal in sorted(group.keys())]
    post_values = [group[animal]['post'] for animal in sorted(group.keys())]

    fig, ax = plt.subplots()
    # Plot each animal's pre and post as points and connect them
    for pre, post in zip(pre_values, post_values):
        ax.plot([0, 1], [pre, post], marker='o', color='black', linestyle='-')

    # Add a horizontal line at ratio = 1
    ax.axhline(y=1, color='gray', linestyle='--', linewidth=1)

    ax.set_xticks([0, 1])
    ax.set_xticklabels(labels)
    ax.set_title(title)
    ax.set_ylabel('Ratio of Paired to Unpaired Licks')

    plt.show()

# Plot both groups
plot_aggregated_group(group1, 'With Combined Retro/Ortho Olfactory Exposure (n=4)')
plot_aggregated_group(group2, 'Without Combined Retro/Ortho Olfactory Exposure (n=5) ')
