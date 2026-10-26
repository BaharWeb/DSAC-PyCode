import seaborn as sns
import pandas as pd
import matplotlib.pyplot as plt

# Define your data
category_names = ['Irrelevant', 'Poorly relevant', 'Relevant', 'Highly relevant']
results = {
    'Accuracy': [2, 10, 51, 37],
    'Readability': [2, 10, 50, 38]
}

# Convert to long-form DataFrame
data = []
for metric, values in results.items():
    for category, value in zip(category_names, values):
        data.append({'Metric': metric, 'Category': category, 'Value': value})

df = pd.DataFrame(data)

# Set custom color palette
palette = {
    'Irrelevant': '#ff4c4c',
    'Poorly relevant': '#ff9999',
    'Relevant': '#99ff99',
    'Highly relevant': '#32ff32'
}

# Create a barplot using seaborn
plt.figure(figsize=(8, 4))
barplot = sns.barplot(
    data=df,
    x='Metric',
    y='Value',
    hue='Category',
    palette=palette
)

# Annotate bar values
# for container in plt.gca().containers:
#     for bar in container:
#         height = bar.get_height()
#         if height > 0:
#             barplot.text(
#                 bar.get_x() + bar.get_width() / 2,
#                 height + 1,
#                 f'{int(height)}',
#                 ha='center',
#                 va='bottom',
#                 fontsize=8
#             )

# Adjust legend position: below the plot, in one row
plt.legend(
    #title='Category',
    loc='upper center',
    bbox_to_anchor=(0.5, -0.15),
    ncol=len(category_names),
    fontsize='small'
)

plt.ylabel("Count")
#plt.title("Survey Results by Metric and Relevance Category")
plt.tight_layout()
plt.subplots_adjust(bottom=0.25)  # Add space at bottom for legend
plt.show()
