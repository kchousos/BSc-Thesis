import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
from matplotlib.colors import ListedColormap

# Load and prepare data
df = pd.read_csv("benchmark-results.csv")
df.columns = df.columns.str.strip()
project_cols = df.columns[2:]
projects = project_cols.tolist()
runs = df["run"].astype(str).tolist()

# Extract binary outcome matrix [projects x runs]
data = df[project_cols].T.values

# Map data values to color indices: 0 → yellow, 1 → green, NaN → white
plot_data = np.where(np.isnan(data), 2, data.astype(int))

# Define color map
cmap = ListedColormap(["#f7eebe", "#a1f7af"])  # yellow, green

# Create figure and axis
fig, ax = plt.subplots(figsize=(len(runs) * 0.8, len(projects) * 0.6))

# Plot the matrix
im = ax.imshow(plot_data, aspect='auto', cmap=cmap)

# Add grid lines between cells
for i in range(len(projects) + 1):
    ax.axhline(i - 0.5, color='black', linewidth=1)
for j in range(len(runs) + 1):
    ax.axvline(j - 0.5, color='black', linewidth=1)

# Configure ticks
ax.set_xticks(range(len(runs)))
ax.set_xticklabels(runs, rotation=45, ha='right')
ax.set_yticks(range(len(projects)))
ax.set_yticklabels(projects)

# Labels and title
ax.set_xlabel("GitHub Actions Benchmark Run")
ax.set_ylabel("Project")
ax.set_title("OverHAuL Benchmark Results")

# Remove default grid and adjust layout
ax.grid(False)
plt.tight_layout()
plt.show()
