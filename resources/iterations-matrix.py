import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
from matplotlib.colors import Normalize
from matplotlib import cm

# Load iterations CSV
df = pd.read_csv("iterations.csv")
df.columns = df.columns.str.strip()

# Extract runs and project names (keep dateparse, skip only 'run')
runs = df["run"].astype(str).tolist()
projects = [col for col in df.columns if col != "run"]

# Extract data matrix: [projects x runs]
data_raw = df[projects].T  # transpose to get [projects x runs]
data = data_raw.replace("x", np.nan).astype(float).values  # "x" → NaN

# Create colormap (Greens) and normalize 0–10
cmap = cm.get_cmap("Greens", 11)
norm = Normalize(vmin=0, vmax=10)

# Create figure
fig, ax = plt.subplots(figsize=(len(runs) * 0.8, len(projects) * 0.6))

# Create image array (RGBA), default to white
image = np.full((len(projects), len(runs), 4), fill_value=1.0)

# Fill image with color based on iteration value
for i in range(len(projects)):
    for j in range(len(runs)):
        val = data[i, j]
        if not np.isnan(val):
            image[i, j] = cmap(norm(val))

# Plot the image
im = ax.imshow(image, aspect='auto')

# Draw grid lines
for i in range(len(projects) + 1):
    ax.axhline(i - 0.5, color='black', linewidth=1)
for j in range(len(runs) + 1):
    ax.axvline(j - 0.5, color='black', linewidth=1)

# Add iteration - 1 text in each block
for i in range(len(projects)):
    for j in range(len(runs)):
        val = data[i, j]
        if not np.isnan(val):
            ax.text(j, i, str(int(val) - 1), ha='center', va='center', fontsize=8, color='black')

# Set ticks
ax.set_xticks(range(len(runs)))
ax.set_xticklabels(runs, rotation=45, ha='right')
ax.set_yticks(range(len(projects)))
ax.set_yticklabels(projects)

# Labels and title
ax.set_xlabel("GitHub Actions Benchmark Run")
ax.set_ylabel("Project")
ax.set_title("OverHAuL Iterations Heatmap")

# Finalize layout
ax.grid(False)
plt.tight_layout()
plt.show()
