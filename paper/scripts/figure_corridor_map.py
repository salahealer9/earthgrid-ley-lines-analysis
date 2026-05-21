#!/usr/bin/env python3
"""
figure_corridor_map.py

Figure 1 — Map of southern Britain showing the canonical Michael ley line
corridor (great circle through pole +33.330°, -147.354°), the 130 named
canonical sites from the source KML, and the testing bounding box.

The production version on a desktop with cartopy installed would add real
coastlines via cfeature.COASTLINE. Without cartopy this version uses a
PlateCarree-equivalent equirectangular projection (raw lat/lon) and lets
the dense distribution of canonical sites along the British coast trace
out the geography by itself.
"""
import csv
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle

R_EARTH_KM = 6371.0

def latlon_to_xyz(lat_deg, lon_deg):
    lat = np.radians(lat_deg); lon = np.radians(lon_deg)
    return np.array([np.cos(lat)*np.cos(lon), np.cos(lat)*np.sin(lon), np.sin(lat)])

def great_circle_points(pole_lat, pole_lon, n=720):
    pole = latlon_to_xyz(pole_lat, pole_lon)
    e = np.array([1.0, 0.0, 0.0]) if abs(pole[0]) < 0.9 else np.array([0.0, 1.0, 0.0])
    u = e - np.dot(e, pole) * pole;  u /= np.linalg.norm(u)
    v = np.cross(pole, u)
    t = np.linspace(0, 2 * np.pi, n)
    pts = np.cos(t)[:, None] * u[None, :] + np.sin(t)[:, None] * v[None, :]
    lats = np.degrees(np.arcsin(np.clip(pts[:, 2], -1, 1)))
    lons = np.degrees(np.arctan2(pts[:, 1], pts[:, 0]))
    return lats, lons

# Load the 130 canonical sites
sites = []
with open('data/ley_lines/michael_ley_line/st_michaels_all_130.csv') as f:
    for r in csv.DictReader(f):
        try:
            sites.append((r['name'], float(r['lat']), float(r['lon'])))
        except (ValueError, KeyError):
            pass
site_lats = np.array([s[1] for s in sites])
site_lons = np.array([s[2] for s in sites])

labelled = {
    "St Michael's Mount": (50.116, -5.477),
    "Glastonbury Tor":    (51.144, -2.696),
    "Avebury":            (51.428, -1.854),
    "Burgh St Peter":     (52.484,  1.681),
}

# Custom offsets for labels (X, Y) — negative Y moves labels below the line
label_offsets = {
    "St Michael's Mount": (8, -15),
    "Glastonbury Tor":    (8, -18),
    "Avebury":            (8, -18),
    "Burgh St Peter":     (-10, -15),
}

bbox_lat = (49.5, 53.5)
bbox_lon = (-6.5, 2.5)

fig, ax = plt.subplots(figsize=(11, 6.5))
ax.set_facecolor('#f4f1ec')

# View slightly larger than the bbox
view_pad = 0.8
ax.set_xlim(bbox_lon[0] - view_pad, bbox_lon[1] + view_pad)
ax.set_ylim(bbox_lat[0] - view_pad, bbox_lat[1] + view_pad)

# Bounding box
ax.add_patch(Rectangle(
    (bbox_lon[0], bbox_lat[0]),
    bbox_lon[1] - bbox_lon[0],
    bbox_lat[1] - bbox_lat[0],
    fill=False, edgecolor='#666', linewidth=1.2, linestyle='--', alpha=0.8,
    label='Test region (bounding box)'
))

# Canonical great circle, trimmed to the view
gc_lats, gc_lons = great_circle_points(33.330, -147.354, n=2000)
mask = (gc_lons > bbox_lon[0] - 1.5) & (gc_lons < bbox_lon[1] + 1.5) & \
       (gc_lats > bbox_lat[0] - 1.5) & (gc_lats < bbox_lat[1] + 1.5)
ax.plot(gc_lons[mask], gc_lats[mask], color='#d62728',
        linewidth=2.5, alpha=0.9, label='Canonical Michael corridor', zorder=4)

# 130 named sites
ax.scatter(site_lons, site_lats, s=12, color='#1f77b4', alpha=0.65,
           edgecolors='white', linewidths=0.5,
           label=f'{len(sites)} canonical sites (KML)', zorder=5)

# Labelled subset with smaller stars and labels below the line
for name, (lat, lon) in labelled.items():
    offset_x, offset_y = label_offsets.get(name, (8, -15))
    ax.plot(lon, lat, marker='*', markersize=8, color='gold',
            markeredgecolor='black', markeredgewidth=0.5, zorder=10)
    ax.annotate(
        name, xy=(lon, lat), xytext=(offset_x, offset_y), textcoords='offset points',
        fontsize=9, zorder=11,
        bbox=dict(boxstyle='round,pad=0.25', facecolor='white',
                  edgecolor='gray', alpha=0.9)
    )

ax.set_xlabel('Longitude (° E)')
ax.set_ylabel('Latitude (° N)')
ax.set_aspect(1 / np.cos(np.radians(51.5)))  # equirectangular at mid-latitude
ax.grid(True, alpha=0.3, linewidth=0.4)
ax.legend(loc='upper left', framealpha=0.95, fontsize=9.5)
ax.set_title(
    'Figure 1: Canonical Michael ley line corridor over southern Britain\n'
    r'bounding box 49.5–53.5° N, 6.5° W – 2.5° E; pole $(+33.330°, -147.354°)$',
    fontsize=11
)

plt.tight_layout()
plt.savefig('paper/figures/figure1_corridor_map.png', dpi=300, bbox_inches='tight')
plt.savefig('paper/figures/figure1_corridor_map.pdf', bbox_inches='tight')
print(f"Saved paper/figure1_corridor_map.{{png,pdf}}; plotted {len(sites)} canonical sites")