import matplotlib.pyplot as plt
import numpy as np

# Semantic similarity thresholds
semantic_sim = [0.55, 0.6, 0.65]
precision = [0.47, 0.9, 0.8]
recall = [0.66, 0.84, 0.6]

x = np.arange(len(semantic_sim))
bar_width = 0.2  # Smaller bar width

# Smaller figure size
fig, ax = plt.subplots(figsize=(5, 4))

# Plot bars
bars1 = ax.bar(x - bar_width/2, precision, bar_width, label='Precision', color='steelblue')
bars2 = ax.bar(x + bar_width/2, recall, bar_width, label='Recall', color='coral')

# Axis labels and ticks
ax.set_xlabel('Semantic Similarity Threshold', fontsize=10)
ax.set_ylabel('Score', fontsize=10)
ax.set_title('Precision and Recall by Threshold', fontsize=11)
ax.set_xticks(x)
ax.set_xticklabels(semantic_sim)
ax.set_ylim(0, 1.1)
ax.legend(fontsize=9)

# Annotate bars with values
for bars in [bars1, bars2]:
    for bar in bars:
        height = bar.get_height()
        ax.annotate(f'{height:.2f}',
                    xy=(bar.get_x() + bar.get_width() / 2, height),
                    xytext=(0, 2),
                    textcoords='offset points',
                    ha='center', va='bottom', fontsize=8)

plt.tight_layout()
plt.show()
