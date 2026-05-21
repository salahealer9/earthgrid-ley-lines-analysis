#!/usr/bin/env python3
"""
Figure 1 — Two-panel map for paper:
  Panel A: Canonical Michael corridor + 130 KML sites
  Panel B: Same corridor + reference catalogs (B2, B1, A) as background
  With Cartopy coastlines and borders.

Catalog colors are kept consistent with Figures 2 and 3:
  B1 (prehistoric)        blue   #1f77b4
  A  (Michael churches)   green  #2ca02c
  B2 (broad archaeology)  red    #d62728

The 130 canonical sites in Panel A use orange (#ff7f0e) to distinguish them
from the B1 blue in Panel B.
"""

import csv
import numpy as np
import matplotlib.pyplot as plt
import cartopy.crs as ccrs
import cartopy.feature as cfeature

R_EARTH_KM = 6371.0

# ---- Consistent catalog colors across all paper figures -------------------
COLOR_B1 = '#1f77b4'   # blue
COLOR_A  = '#2ca02c'   # green
COLOR_B2 = '#d62728'   # red
COLOR_130 = '#ff7f0e'  # orange (distinct from any catalog color)
COLOR_CORRIDOR = '#000000'  # black for the canonical corridor in Panel B
                            # (red would clash with B2; black reads cleanly
                            # over the catalog point clouds)


def latlon_to_xyz(lat_deg, lon_deg):
    lat = np.radians(lat_deg); lon = np.radians(lon_deg)
    return np.array([np.cos(lat)*np.cos(lon), np.cos(lat)*np.sin(lon), np.sin(lat)])

def great_circle_points(pole_lat, pole_lon, n=720):
    pole = latlon_to_xyz(pole_lat, pole_lon)
    e = np.array([1.0, 0.0, 0.0]) if abs(pole[0]) < 0.9 else np.array([0.0, 1.0, 0.0])
    u = e - np.dot(e, pole) * pole
    u /= np.linalg.norm(u)
    v = np.cross(pole, u)
    t = np.linspace(0, 2 * np.pi, n)
    pts = np.cos(t)[:, None] * u[None, :] + np.sin(t)[:, None] * v[None, :]
    lats = np.degrees(np.arcsin(np.clip(pts[:, 2], -1, 1)))
    lons = np.degrees(np.arctan2(pts[:, 1], pts[:, 0]))
    return lats, lons

def load_sites(csv_path, lat_col='lat', lon_col='lon'):
    sites = []
    try:
        with open(csv_path) as f:
            for r in csv.DictReader(f):
                try:
                    sites.append((float(r[lat_col]), float(r[lon_col])))
                except (ValueError, KeyError):
                    pass
    except FileNotFoundError:
        print(f"Warning: {csv_path} not found")
    return np.array(sites) if sites else np.empty((0, 2))

# Constants
bbox_lat = (49.5, 53.5)
bbox_lon = (-6.5, 2.5)
pole_lat, pole_lon = 33.330, -147.354

# Load data
sites_130 = load_sites('data/ley_lines/michael_ley_line/st_michaels_all_130.csv')
sites_B1  = load_sites('data/population/catalog_B1_strict.csv')
sites_A   = load_sites('data/population/catalog_A_michael.csv')
sites_B2  = load_sites('data/population/catalog_B2_broad.csv')

# Labelled sites for panel A
labelled = {
    "St Michael's Mount": (50.116, -5.477),
    "Glastonbury Tor":    (51.144, -2.696),
    "Avebury":            (51.428, -1.854),
    "Burgh St Peter":     (52.484,  1.681),
}

# Create two-panel figure with Cartopy projection
fig, (ax1, ax2) = plt.subplots(
    1, 2, figsize=(14, 6.5),
    subplot_kw={'projection': ccrs.PlateCarree()}
)
fig.patch.set_facecolor('#f4f1ec')

def setup_ax(ax, title, corridor_color=COLOR_CORRIDOR):
    """Configure a Cartopy axis with coastlines, borders, bbox, and great circle."""
    ax.set_extent(
        [bbox_lon[0] - 0.8, bbox_lon[1] + 0.8, bbox_lat[0] - 0.8, bbox_lat[1] + 0.8],
        crs=ccrs.PlateCarree()
    )
    ax.add_feature(cfeature.COASTLINE, linewidth=0.8, alpha=0.7)
    ax.add_feature(cfeature.BORDERS, linewidth=0.5, alpha=0.5)
    ax.set_facecolor('#f4f1ec')

    # Bounding box as a line
    bbox_x = [bbox_lon[0], bbox_lon[1], bbox_lon[1], bbox_lon[0], bbox_lon[0]]
    bbox_y = [bbox_lat[0], bbox_lat[0], bbox_lat[1], bbox_lat[1], bbox_lat[0]]
    ax.plot(bbox_x, bbox_y, color='#666', linewidth=1.2, linestyle='--', alpha=0.8,
            transform=ccrs.PlateCarree())

    # Canonical great circle
    gc_lats, gc_lons = great_circle_points(pole_lat, pole_lon, n=2000)
    mask = (gc_lons > bbox_lon[0] - 1.5) & (gc_lons < bbox_lon[1] + 1.5) & \
           (gc_lats > bbox_lat[0] - 1.5) & (gc_lats < bbox_lat[1] + 1.5)
    ax.plot(gc_lons[mask], gc_lats[mask], color=corridor_color,
            linewidth=2.5, alpha=0.9, zorder=4, transform=ccrs.PlateCarree())

    ax.set_xlabel('Longitude (° E)')
    ax.set_ylabel('Latitude (° N)')
    ax.grid(True, alpha=0.3, linewidth=0.4)
    ax.set_title(title, fontsize=10)
    return ax

# ---- Panel A: 130 canonical sites + corridor (red for visibility) ---------
setup_ax(ax1, '(a) 130 canonical sites (KML)', corridor_color='#d62728')

if len(sites_130) > 0:
    ax1.scatter(
        sites_130[:, 1], sites_130[:, 0],
        s=14, color=COLOR_130, alpha=0.75,
        edgecolors='white', linewidths=0.5,
        label=f'{len(sites_130)} sites',
        transform=ccrs.PlateCarree(), zorder=5
    )

# Labelled subset for panel A
label_offsets = {
    "St Michael's Mount": (8, -15),   # below
    "Glastonbury Tor":    (8, -20),   # well below
    "Avebury":            (8, -18),   # below
    "Burgh St Peter":     (-10, -15), # left and below
}

for name, (lat, lon) in labelled.items():
    offset_x, offset_y = label_offsets.get(name, (8, -15))
    ax1.plot(lon, lat, marker='*', markersize=8, color='gold',
             markeredgecolor='black', markeredgewidth=0.5, transform=ccrs.PlateCarree(), zorder=10)
    ax1.annotate(
        name, xy=(lon, lat), xytext=(offset_x, offset_y), textcoords='offset points',
        fontsize=9, zorder=11,
        bbox=dict(boxstyle='round,pad=0.25', facecolor='white', edgecolor='gray', alpha=0.9)
    )

ax1.legend(loc='upper left', framealpha=0.95, fontsize=9)

# ---- Panel B: Reference catalogs (background) -----------------------------
# Plot order: B2 first (largest, faintest), then B1, then A (smallest, on top)
setup_ax(ax2, '(b) Reference catalogs vs canonical corridor',
         corridor_color=COLOR_CORRIDOR)

if len(sites_B2) > 0:
    ax2.scatter(
        sites_B2[:, 1], sites_B2[:, 0],
        s=3, color=COLOR_B2, alpha=0.18,
        edgecolors='none',
        label=f'B2 broad archaeology (N={len(sites_B2)})',
        transform=ccrs.PlateCarree(), zorder=1
    )
if len(sites_B1) > 0:
    ax2.scatter(
        sites_B1[:, 1], sites_B1[:, 0],
        s=5, color=COLOR_B1, alpha=0.40,
        edgecolors='none',
        label=f'B1 prehistoric (N={len(sites_B1)})',
        transform=ccrs.PlateCarree(), zorder=2
    )
if len(sites_A) > 0:
    ax2.scatter(
        sites_A[:, 1], sites_A[:, 0],
        s=7, color=COLOR_A, alpha=0.60,
        edgecolors='none',
        label=f'A Michael churches (N={len(sites_A)})',
        transform=ccrs.PlateCarree(), zorder=3
    )

ax2.legend(loc='upper left', framealpha=0.95, fontsize=9, markerscale=2.5)

# Main title — y just below 1.0 so tight_layout has room
fig.suptitle(
    'Figure 1: Canonical Michael ley line corridor over southern Britain\n'
    r'bounding box 49.5–53.5° N, 6.5° W – 2.5° E; pole $(+33.330°, -147.354°)$',
    fontsize=11, y=0.995
)

plt.tight_layout(rect=[0, 0, 1, 0.95])
plt.savefig('paper/figures/figure1_two_panel.png', dpi=300, bbox_inches='tight')
plt.savefig('paper/figures/figure1_two_panel.pdf', bbox_inches='tight')
print("Saved paper/figures/figure1_two_panel.{png,pdf}")
