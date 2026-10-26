import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np

# Define confusion matrices for each SemanticSim threshold
matrices = {
    'SemanticSim = 0.55': np.array([[157, 10],
                                    [3, 12]]),
    'SemanticSim = 0.6': np.array([[167, 0],
                                   [3, 12]]),
    'SemanticSim = 0.65': np.array([[167, 0],
                                    [7, 8]])
}

labels = ['Negative', 'Positive']

# Create subplots: 1 row, 3 columns
fig, axes = plt.subplots(1, 3, figsize=(12, 4))

for ax, (title, matrix) in zip(axes, matrices.items()):
    sns.heatmap(matrix, annot=True, fmt='d', cmap='Blues',
                xticklabels=labels, yticklabels=labels,
                cbar=False, ax=ax)
    ax.set_title(title)
    ax.set_xlabel('Predicted Label')
    ax.set_ylabel('True Label')

plt.tight_layout()
plt.show()
