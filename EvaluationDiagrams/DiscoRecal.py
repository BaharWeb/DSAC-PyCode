import matplotlib.pyplot as plt
import numpy as np

# Data
tasks = ['Component Identification', 'Domain Identification']
precision = [0.85, 0.85]
recall = [0.78, 0.90]

x = np.array([0, 0.5])  # Adjust this value to reduce spacing
width = 0.05

# Plot
fig, ax = plt.subplots(figsize=(8, 5))
bars1 = ax.bar(x - width/2, precision, width, label='Precision', color='steelblue')
bars2 = ax.bar(x + width/2, recall, width, label='Recall', color='coral')

# Labels
ax.set_ylabel('Score')
ax.set_ylim(0, 1.05)
ax.set_title('Precision and Recall per Task')
ax.set_xticks(x)
ax.set_xticklabels(tasks)
ax.legend(loc='upper center', bbox_to_anchor=(0.5, -0.15), ncol=2)

# Add value labels on bars
for bars in [bars1, bars2]:
    for bar in bars:
        height = bar.get_height()
        ax.annotate(f'{height:.2f}',
                    xy=(bar.get_x() + bar.get_width() / 2, height),
                    xytext=(0, 3),
                    textcoords="offset points",
                    ha='center', va='bottom')

plt.tight_layout()
plt.show()
