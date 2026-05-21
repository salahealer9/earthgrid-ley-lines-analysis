#!/usr/bin/env python3
"""
figure_bearing_trajectory.py

Figure 3 — K_null mean (at w = 5 km) as a function of the bearing-restriction
tolerance angle, for the three reference catalogs. The flat trajectory across
all four tolerances visualizes the absence of orientation confound.

Data sourced from the bearing-restricted population test runs (Section 3.3).
"""
import matplotlib.pyplot as plt
import numpy as np

# Bearing tolerances. "Isotropic" plotted as 90° (= no bearing restriction).
tolerances = [90, 30, 15, 5]

# K_null mean at w = 5 km from the per-catalog runs
b1 = [31.31, 31.45, 31.09, 31.26]
a  = [9.87, 9.81, 9.68, 9.75]
b2 = [71.64, 71.39, 70.67, 71.04]

fig, axes = plt.subplots(1, 3, figsize=(11.5, 3.5), sharex=False)

for ax, vals, label, color, ymid in zip(
    axes, [b1, a, b2],
    ['B1 — prehistoric (N = 2422)', 'A — Michael churches (N = 754)', 'B2 — broad archaeological (N = 5500)'],
    ['#1f77b4', '#2ca02c', '#d62728'],
    [31.3, 9.8, 71.3]
):
    ax.plot(tolerances, vals, 'o-', color=color, markersize=8, linewidth=1.5)
    ax.set_xscale('log')
    ax.set_xticks(tolerances)
    ax.set_xticklabels(['iso (90°)', '±30°', '±15°', '±5°'])
    ax.invert_xaxis()
    ax.set_xlabel('Bearing tolerance')
    ax.set_ylabel(r'$K_{\mathrm{null}}$ mean at $w = 5$ km')
    ax.set_title(label, fontsize=10)
    # Tight y-range to show the flatness
    span = max(vals) - min(vals)
    margin = max(span * 3, 0.5)
    ax.set_ylim(ymid - margin, ymid + margin)
    ax.grid(True, alpha=0.3)
    # Annotate the range
    ax.text(
        0.95, 0.95,
        f'range = {max(vals) - min(vals):.2f}',
        transform=ax.transAxes, fontsize=9, ha='right', va='top',
        bbox=dict(boxstyle='round,pad=0.3', facecolor='white', edgecolor='gray', alpha=0.85)
    )

plt.suptitle(
    r'Figure 3: $K_{\mathrm{null}}$ mean is invariant across bearing tolerances '
    r'(no orientation confound)',
    fontsize=11, y=1.02
)
plt.tight_layout()
plt.savefig('paper/figures/figure3_bearing_trajectory.png', dpi=300, bbox_inches='tight')
plt.savefig('paper/figures/figure3_bearing_trajectory.pdf', bbox_inches='tight')
print("Saved paper/figure3_bearing_trajectory.{png,pdf}")
