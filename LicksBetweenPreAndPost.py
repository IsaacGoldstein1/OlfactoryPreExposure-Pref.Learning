import pandas as pd
import matplotlib.pyplot as plt
import io

# Function to process the dataset
def process_data(data):
    # Use StringIO to handle the data as if it was a file
    data_io = io.StringIO(data.iloc[0,0] + '\n' + '\n'.join(data.iloc[1:,0]))
    # Read the dataset with correct parsing
    df = pd.read_csv(data_io)
    return df

# Load and process the data
file_pre = '/Users/isaac/Documents/Extra/0128GW05_pretest.ms8 copy.txt'
file_post = '/Users/isaac/Documents/Extra/0205GW05_test1.ms8 copy.txt'
data_pre = pd.read_csv(file_pre, sep='\t', header=None)
data_post = pd.read_csv(file_post, sep='\t', header=None)
processed_data_pre = process_data(data_pre)
processed_data_post = process_data(data_post)

# Clean up the column names
processed_data_pre.columns = processed_data_pre.columns.str.strip()
processed_data_post.columns = processed_data_post.columns.str.strip()

# Define the tube groupings for each odor
odor_tubes = {
    'Water': [1, 2],
    'Carvone': [3, 4],
    'cis3hex': [5, 6]
}

# Function to calculate average licks per odor
def average_licks(data):
    averages = {}
    for odor, tubes in odor_tubes.items():
        filtered_data = data[data['TUBE'].isin(tubes)]
        average_licks = filtered_data['LICKS'].mean()
        averages[odor] = average_licks
    return averages

# Calculate average licks for pre and post data
average_licks_pre = average_licks(processed_data_pre)
average_licks_post = average_licks(processed_data_post)

# Plotting the results
labels = list(average_licks_pre.keys())
pre_values = list(average_licks_pre.values())
post_values = list(average_licks_post.values())

x = range(len(labels))  # the label locations
width = 0.35  # the width of the bars

fig, ax = plt.subplots()
rects1 = ax.bar(x, pre_values, width, label='Pre')
rects2 = ax.bar([p + width for p in x], post_values, width, label='Post')

# Add some text for labels, title and custom x-axis tick labels, etc.
ax.set_ylabel('Average Licks')
ax.set_title('Average Number of Licks per Trial by Odor')
ax.set_xticks([p + width / 2 for p in x])
ax.set_xticklabels(labels)
ax.legend()

# Function to attach a text label above each bar in *rects*
def autolabel(rects):
    for rect in rects:
        height = rect.get_height()
        ax.annotate('{}'.format(round(height, 2)),
                    xy=(rect.get_x() + rect.get_width() / 2, height),
                    xytext=(0, 3),  # 3 points vertical offset
                    textcoords="offset points",
                    ha='center', va='bottom')

autolabel(rects1)
autolabel(rects2)

plt.show()
