import matplotlib.pyplot as plt
import numpy as np
from matplotlib.colors import to_rgba
from matplotlib.patches import Patch

category_names = ['Irrelevant', 'Poorly relevant', 'Relevant', 'Highly relevant']
results = {
    'Domain Identification': [5, 10, 35, 50],
    'Component Identification': [10, 15, 45, 30]
}

def survey(results, category_names):
    labels = list(results.keys())
    data = np.array(list(results.values()))
    data_cum = data.cumsum(axis=1)
    total = np.sum(data, axis=1).max()
    
    # Custom category colors
    category_colors = [
        to_rgba('#ff4c4c', 1.0),  # red
        to_rgba('#ff9999', 1.0),  # light red
        to_rgba('#99ff99', 1.0),  # light green
        to_rgba('#32ff32', 1.0)   # green
    ]

    fig, axs = plt.subplots(nrows=len(labels), figsize=(9.2, 1.1 * len(labels)))

    # Handle single vs multiple axes
    if len(labels) == 1:
        axs = [axs]

    for ax, label, row, row_cum in zip(axs, labels, data, data_cum):
        ax.invert_yaxis()
        ax.set_xlim(0, total)
        ax.set_yticks([])
        ax.set_xticks([])

        ax.text(-5, 0, label, va='center', ha='right', fontsize=10)

        for i, (colname, color) in enumerate(zip(category_names, category_colors)):
            width = row[i]
            start = row_cum[i] - width
            ax.barh([0], [width], left=[start], height=0.2, label=colname if label == labels[0] else "", color=color)

        # Add percentage axis below
        secax = ax.secondary_xaxis('bottom')
        secax.set_xlim(0, total)
        secax.set_xticks(np.linspace(0, total, 11))
        secax.set_xticklabels([f"{int((x / total) * 100)}%" for x in np.linspace(0, total, 11)])

    # Add legend once under the last subplot
    axs[-1].legend(
        handles=[
            Patch(facecolor=category_colors[i], label=category_names[i])
            for i in range(len(category_names))
        ],
        ncols=len(category_names),
        loc='upper center',
        bbox_to_anchor=(0.5, -0.5),
        fontsize='small'
)

    plt.tight_layout()
    plt.subplots_adjust(bottom=0.25)  # Give space for legend
    return fig, axs

survey(results, category_names)
plt.show()
