import matplotlib.pyplot as plt
import numpy as np

Domains = ['Academic', 'Travel', 'Online Shop']
precision = [0.80, 0.80, 0.82]
recall = [0.90, 0.80, 0.90]
f1 = [0.85, 0.80, 0.86]

x = np.arange(len(Domains))
bar_width = 0.2

# Smaller figure size
fig, ax = plt.subplots(figsize=(6, 4))

# Plot bars
bars1 = ax.bar(x - bar_width, precision, bar_width, label='Precision', color='steelblue')
bars2 = ax.bar(x, recall, bar_width, label='Recall', color='coral')
bars3 = ax.bar(x + bar_width, f1, bar_width, label='F1 Score', color='seagreen')


# Axis labels and ticks
#ax.set_xlabel('Semantic Similarity Threshold', fontsize=10)
ax.set_ylabel('Score', fontsize=10)
#ax.set_title('Precision and Recall by Threshold', fontsize=11)
ax.set_xticks(x)
ax.set_xticklabels(Domains)
ax.set_ylim(0, 1)
#ax.legend(fontsize=9)
ax.legend(loc='upper center', bbox_to_anchor=(0.5, -0.15), ncol=3, fontsize=9)


# Annotate bars with values
# for bars in [bars1, bars2]:
#     for bar in bars:
#         height = bar.get_height()
#         ax.annotate(f'{height:.2f}',
#                     xy=(bar.get_x() + bar.get_width() / 2, height),
#                     xytext=(0, 2),
#                     textcoords='offset points',
#                     ha='center', va='bottom', fontsize=8)

plt.tight_layout()
plt.show()
