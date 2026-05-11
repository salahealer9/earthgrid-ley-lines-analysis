# Map showing the two currents (Michael and Mary) plotted in detail across the UK. The map has four layers: The Michael alignment (Blue), The Mary # current (Green) and The Michael current (Red) and markers layer with links to paintings.
# 345,257 views
# Published on September 27, 2017
# Source: https://www.google.com/maps/d/u/0/viewer?mid=1EfTggFzl0UQ1W_Ls45K2Cl_H6eE&hl=en_US&utm_source=Pinterest&utm_medium=organic

#!/usr/bin/env python3
"""
extract_kml_placemarks.py

Extract all Placemark coordinates from a KML file and save as CSV.
"""

import xml.etree.ElementTree as ET
import csv
import sys
import os
from pathlib import Path

NS = {"kml": "http://www.opengis.net/kml/2.2"}


def extract_placemarks(kml_path: str) -> list[tuple]:
    """Extract (name, lat, lon) from all Placemarks in a KML file."""
    tree = ET.parse(kml_path)
    root = tree.getroot()

    sites = []

    for pm in root.findall(".//kml:Placemark", NS):
        # Get name
        name_elem = pm.find("kml:name", NS)
        name = name_elem.text if name_elem is not None else "Unknown"

        # Get coordinates (try Point, then LineString's centroid? For now only Point)
        coords_elem = pm.find(".//kml:Point/kml:coordinates", NS)
        if coords_elem is not None and coords_elem.text:
            coords = coords_elem.text.strip().split(",")
            if len(coords) >= 2:
                lon, lat = float(coords[0]), float(coords[1])
                sites.append((name, lat, lon))

    return sites


def save_csv(sites: list[tuple], output_path: str) -> None:
    """Save sites to CSV with columns: name, lat, lon."""
    with open(output_path, "w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow(["name", "lat", "lon"])
        writer.writerows(sites)
    print(f"Saved {len(sites)} sites to {output_path}")


def main():
    if len(sys.argv) < 2:
        print("Usage: python extract_kml_placemarks.py <kml_file> [output_csv]")
        sys.exit(1)

    kml_path = sys.argv[1]
    output_path = sys.argv[2] if len(sys.argv) > 2 else "extracted_sites.csv"

    if not os.path.exists(kml_path):
        print(f"Error: File not found: {kml_path}")
        sys.exit(1)

    sites = extract_placemarks(kml_path)
    save_csv(sites, output_path)

    # Print first few for sanity
    print("\nFirst 5 sites:")
    for name, lat, lon in sites[:5]:
        print(f"  {name}: ({lat:.6f}, {lon:.6f})")


if __name__ == "__main__":
    main()