import matplotlib.pyplot as plt

# Data
technical_labels = ['Basic', 'Intermediate', 'Advanced', 'Developer']
technical_sizes = [6, 10, 5, 2]
technical_colors = ['#ff9999','#66b3ff','#99ff99','#ffcc99']

age_labels = ['18-25', '25-30', '30-40', '40-50']
age_sizes = [7, 3, 10, 3]
age_colors = ['#c2c2f0','#ffb3e6','#c2f0c2','#ffccff']

experience_labels = ['Yes', 'No']
experience_sizes = [5, 18]
experience_colors = ['#8dd3c7', '#fb8072']

# Setup figure
fig, axs = plt.subplots(1, 3, figsize=(10, 4))

# Function for donut chart
def donut_chart(ax, sizes, labels, colors, center_title):
    ax.pie(sizes, labels=labels, colors=colors, startangle=90, wedgeprops={'width': 0.4})
    ax.axis('equal')
    ax.text(0, 0, center_title, ha='center', va='center', fontsize=10, weight='bold')

# Draw the charts
donut_chart(axs[0], technical_sizes, technical_labels, technical_colors, "Technical\nExpertise")
donut_chart(axs[1], age_sizes, age_labels, age_colors, "Age\nGroup")
donut_chart(axs[2], experience_sizes, experience_labels, experience_colors, "Prior\nExperience")

plt.tight_layout()
plt.show()
