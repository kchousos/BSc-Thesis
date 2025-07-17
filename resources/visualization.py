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

# Insert NaN columns between each run for spacing
spaced_data = []
for col in data.T:
    spaced_data.append(col[:, None])                                # actual run
    spaced_data.append(np.full((len(projects), 1), np.nan))         # spacer

spaced_matrix = np.hstack(spaced_data[:-1])  # exclude last spacer

# Map data values to color indices: 0 → yellow, 1 → green, NaN → white
plot_data = np.where(np.isnan(spaced_matrix), 2, spaced_matrix.astype(int))

# Define color map
cmap = ListedColormap(["#FFD700", "#2ECC71", "#FFFFFF"])  # yellow, green, white

# Plot
# plt.figure(figsize=(len(runs) * 0.7, len(projects) * 0.5))
plt.figure()
plt.imshow(plot_data, aspect='auto', cmap=cmap)

# Configure ticks
x_ticks = [i for i in range(0, plot_data.shape[1], 2)]
x_labels = runs
plt.xticks(ticks=x_ticks, labels=x_labels, rotation=45, ha='right')
plt.yticks(ticks=range(len(projects)), labels=projects)

# Labels and title
plt.xlabel("GitHub Actions Benchmark Run")
plt.ylabel("Project")
plt.title("OverHAuL Benchmark Results")
# plt.grid(False)
plt.tight_layout()
plt.show()
