#!/usr/bin/env python3
"""
figure_joint_null.py

Figure 2 — K_null distributions at w = 50 km for the three reference catalogs,
under the isotropic population null. The canonical Michael corridor's K_real
is marked with a vertical line; the small number of null trials at or above
K_real visualizes the joint conjunction p_joint = 0.0002.

Data sourced from triple_corridor_test.py trials.csv output (Section 3.4).
Now loads the actual trials.csv to show the true right-skewed distribution.
"""

import matplotlib.pyplot as plt
import pandas as pd
import numpy as np

# Load the actual trials data (isotropic null, combined pole)
# Adjust path as needed — using the triple_combined_pole trials file
trials_file = 'results_corridor/population/triple_canonical130_iso.trials.csv'

try:
    df = pd.read_csv(trials_file)
    print(f"Loaded {len(df)} trials from {trials_file}")
except FileNotFoundError:
    # Fallback: try the michael pole file
    trials_file = 'results_corridor/population/triple_michael_pole.trials.csv'
    df = pd.read_csv(trials_file)
    print(f"Loaded {len(df)} trials from {trials_file}")

# Extract K values at w = 50 km
# Column names are 'K_B1_w50.0', 'K_A_w50.0', 'K_B2_w50.0'
K_B1 = df['K_B1_w50.0'].values
K_A = df['K_A_w50.0'].values
K_B2 = df['K_B2_w50.0'].values

# K_real values (canonical corridor at w=50km from Results 3.2)
K_real = {
    'B1': 1261,
    'A': 325,
    'B2': 2635,
}

# Catalog labels and colors
catalogs = [
    ('B1 — prehistoric monuments\n(N = 2422)', K_B1, 1261, '#1f77b4'),
    ('A — Michael church dedications\n(N = 754)', K_A, 325, '#2ca02c'),
    ('B2 — broad archaeological\n(N = 5500)', K_B2, 2635, '#d62728'),
]

fig, axes = plt.subplots(1, 3, figsize=(13, 4))
T = len(df)

for ax, (label, K_null, K_real_val, color) in zip(axes, catalogs):
    # Calculate statistics from actual data
    mean = np.mean(K_null)
    std = np.std(K_null)
    tail = np.sum(K_null >= K_real_val)
    
    # Set x-axis limits with some padding
    K_max = max(K_real_val * 1.1, np.percentile(K_null, 99.5))
    bins = np.linspace(0, K_max, 50)
    
    # Plot histogram
    ax.hist(K_null, bins=bins, color=color, alpha=0.7, edgecolor='white', linewidth=0.4)
    ax.axvline(K_real_val, color='black', linewidth=2, linestyle='-')
    
    # Annotate K_real on the line
    ymax = ax.get_ylim()[1]
    ax.text(K_real_val, ymax * 0.97, f'  $K_{{\\mathrm{{real}}}} = {K_real_val}$',
            fontsize=9.5, ha='left', va='top', fontweight='bold')
    
    # Info box with empirical stats
    ax.text(
        0.97, 0.85,
        f'$K_{{\\mathrm{{null}}}}$ mean ± SD: {mean:.0f} ± {std:.0f}\n'
        f'trials with $K_t \\geq K_{{\\mathrm{{real}}}}$: {tail} / {T}',
        transform=ax.transAxes, fontsize=9, ha='right', va='top',
        bbox=dict(boxstyle='round,pad=0.4', facecolor='white', edgecolor='gray', alpha=0.9)
    )
    
    ax.set_xlabel(r'$K$ (sites within 50 km of corridor)')
    ax.set_ylabel('null trials' if ax is axes[0] else '')
    ax.set_title(label, fontsize=10)
    ax.set_xlim(0, K_max)
    ax.grid(True, alpha=0.3, axis='y')

# Joint conjunction p-value from Results 3.4
p_joint = 0.0002

plt.suptitle(
    f'Figure 2: $K_{{\\mathrm{{null}}}}$ distributions at $w = 50$ km '
    f'(joint conjunction $p_{{\\mathrm{{joint}}}} = {p_joint}$)',
    fontsize=11, y=1.00
)

plt.tight_layout()
plt.savefig('paper/figures/figure2_joint_null.png', dpi=300, bbox_inches='tight')
plt.savefig('paper/figures/figure2_joint_null.pdf', bbox_inches='tight')
print("Saved paper/figures/figure2_joint_null.{png,pdf}")