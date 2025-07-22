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

# Map values to indices:
# -2 → 0 (orange)
#  0 → 1 (yellow)
#  1 → 2 (green)
# NaN → 3 (white)
plot_data = np.full_like(data, fill_value=3, dtype=int)  # default to 3 (white for NaN)
plot_data[data == -2] = 0
plot_data[data == 0] = 1
plot_data[data == 1] = 2

# Define color map: orange, yellow, green
cmap = ListedColormap([
    "#d98c3b",  # orange (crash in harness, -2)
    "#f5e482",  # yellow (crash not found, 0)
    "#abe697",  # green (pass, 1)
])

# Create figure and axis
fig, ax = plt.subplots(figsize=(len(runs) * 0.8, len(projects) * 0.6))

# Plot the matrix
im = ax.imshow(plot_data, aspect='auto', cmap=cmap)

# Add grid lines between cells
for i in range(len(projects) + 1):
    ax.axhline(i - 0.5, color='black', linewidth=1)
for j in range(len(runs) + 1):
    ax.axvline(j - 0.5, color='black', linewidth=1)

# Add text annotations (-2, 0, or 1)
for i in range(len(projects)):
    for j in range(len(runs)):
        val = data[i, j]
        if not np.isnan(val):
            ax.text(j, i, str(int(val)), ha='center', va='center', fontsize=8, color='black')

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
