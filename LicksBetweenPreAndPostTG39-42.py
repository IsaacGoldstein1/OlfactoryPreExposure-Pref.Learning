import pandas as pd
import matplotlib.pyplot as plt
import io
import numpy as np

# Function to process the dataset
def process_data(data):
    data_io = io.StringIO(data.iloc[0,0] + '\n' + '\n'.join(data.iloc[1:,0]))
    df = pd.read_csv(data_io)
    return df

# Define paths to your files for each animal and both tests
files = {
    'TG39_pre': '/Users/isaac/Desktop/BAT Unsugerized data/0205TG39PREORTHO(UE).ms8 copy.txt',
    'TG39_post': '/Users/isaac/Desktop/BAT Unsugerized data/0212TG39_POSTORTHO(UE).ms8 copy.txt',
    'TG40_pre': '/Users/isaac/Desktop/BAT Unsugerized data/0206TG40PREORTHO(UE).ms8 copy.txt',
    'TG40_post': '/Users/isaac/Desktop/BAT Unsugerized data/post0214TG40POSTORTHO(UE).ms8 copy.txt',
    'TG41_pre': '/Users/isaac/Desktop/BAT Unsugerized data/0310TG41PREORTHO(UE).ms8 copy.txt',
    'TG41_post': '/Users/isaac/Desktop/BAT Unsugerized data/0317TG41_POSTORTHO(UE).ms8 copy.txt',
    'TG42_pre': '/Users/isaac/Desktop/BAT Unsugerized data/0310TG42PREORTHO(UE).ms8 copy.txt',
    'TG42_post': '/Users/isaac/Desktop/BAT Unsugerized data/0324TG42POSTORTHO(UE).ms8 copy.txt'
}
# Load and process data for all files
data = {key: process_data(pd.read_csv(file, sep='\t', header=None)) for key, file in files.items()}

# Clean up column names
for df in data.values():
    df.columns = df.columns.str.strip()

# Odor pairings
odor_tubes = {
    'Paired': [1, 3],
    'Unpaired': [2, 4]
}

# Function to calculate average licks per odor pairing for each animal
def average_licks(data):
    averages = {}
    for pairing, tubes in odor_tubes.items():
        filtered_data = data[data['TUBE'].isin(tubes)]
        average_licks = filtered_data['LICKS'].mean()
        averages[pairing] = average_licks
    return averages

# Calculate average licks for each dataset
average_licks_data = {key: average_licks(df) for key, df in data.items()}

# Calculate group averages and individual points
group_data = {}
individual_points = {}
for condition in ['Paired', 'Unpaired']:
    group_data[condition] = {
        'pre': np.mean([average_licks_data[f'{animal}_pre'][condition] for animal in ['TG39', 'TG40', 'TG41', 'TG42']]),
        'post': np.mean([average_licks_data[f'{animal}_post'][condition] for animal in ['TG39', 'TG40', 'TG41', 'TG42']])
    }
    individual_points[condition] = {
        'pre': [average_licks_data[f'{animal}_pre'][condition] for animal in ['TG39', 'TG40', 'TG41', 'TG42']],
        'post': [average_licks_data[f'{animal}_post'][condition] for animal in ['TG39', 'TG40', 'TG41', 'TG42']]
    }

# Plotting the results
labels = ['Paired', 'Unpaired']
x = np.arange(len(labels))  # the label locations
width = 0.35  # the width of the bars

fig, ax = plt.subplots(figsize=(10, 6))

# Define colors
colors = {
    'Paired_pre': 'lightblue',
    'Paired_post': 'darkblue',
    'Unpaired_pre': 'lightblue',
    'Unpaired_post': 'darkblue'
}

# Plotting for paired and unpaired
for i, condition in enumerate(labels):
    offset = i * width
    y_pre = group_data[condition]['pre']
    y_post = group_data[condition]['post']
    ax.bar(x[i] - width/4, y_pre, width/2, label=f'{condition} Pre', color=colors[f'{condition}_pre'])
    ax.bar(x[i] + width/4, y_post, width/2, label=f'{condition} Post', color=colors[f'{condition}_post'])

    # Plot individual points
    pre_points = individual_points[condition]['pre']
    post_points = individual_points[condition]['post']
    pre_x = np.full(len(pre_points), x[i] - width/4)
    post_x = np.full(len(post_points), x[i] + width/4)
    ax.scatter(pre_x, pre_points, color='black')
    ax.scatter(post_x, post_points, color='black')

    # Connect points with lines
    for pre_pt, post_pt in zip(pre_points, post_points):
        ax.plot([pre_x[0], post_x[0]], [pre_pt, post_pt], 'k-')

ax.set_ylabel('Average Licks')
ax.set_title('Average Licks -- Combined Retro/Ortho Olfactory Exposure')
ax.set_xticks(x)
ax.set_xticklabels(labels)
ax.legend()

plt.show()