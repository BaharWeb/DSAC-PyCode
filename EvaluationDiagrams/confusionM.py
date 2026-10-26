import matplotlib.pyplot as plt
import numpy as np

# Threshold values
thresholds = ['0.55', '0.6', '0.65']

# Confusion matrix values from your data
TP = [10, 12, 8]
FP = [10, 0, 0]
FN = [5, 3, 7]
TN = [147, 157, 161]

# Bar chart setup
x = np.arange(len(thresholds))
width = 0.2

fig, ax = plt.subplots(figsize=(10, 6))
colors = {'TP': '#FFAF00', 'FP': '#F46920', 'FN': '#F53255', 'TN': '#F857C1'}


ax.bar(x - 1.5*width, TP, width, label='TP', color=colors['TP'])
ax.bar(x - 0.5*width, FP, width, label='FP', color=colors['FP'])
ax.bar(x + 0.5*width, FN, width, label='FN', color=colors['FN'])
ax.bar(x + 1.5*width, TN, width, label='TN', color=colors['TN'])


# Labels and styling
ax.set_xlabel('Semantic Similarity Threshold')
ax.set_ylabel('Count')
ax.set_title('Confusion Matrix Counts Across Thresholds')
ax.set_xticks(x)
ax.set_xticklabels(thresholds)
ax.legend()
#ax.grid(axis='y')
ax.grid(False)

plt.tight_layout()
plt.show()
