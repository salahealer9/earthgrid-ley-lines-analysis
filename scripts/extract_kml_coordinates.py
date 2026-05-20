#!/usr/bin/env python3
"""
Extract Michael and Mary current coordinates from KML file.
"""

import xml.etree.ElementTree as ET
import pandas as pd
import os
from pathlib import Path

# Paths
PROJECT_ROOT = Path(__file__).parent.parent
KML_FILE = PROJECT_ROOT / "data" / "michael_ley_line" / "st_michael_line.kml"
OUTPUT_DIR = PROJECT_ROOT / "data" / "ley_lines" / "michael_ley_line"

def extract_coordinates_from_kml(kml_path, folder_name):
    """Extract all lat/lon from LineString elements in a named folder"""
    coords = []
    
    tree = ET.parse(kml_path)
    root = tree.getroot()
    ns = {'kml': 'http://www.opengis.net/kml/2.2'}
    
    for folder in root.findall('.//kml:Folder', ns):
        name_elem = folder.find('.//kml:name', ns)
        if name_elem is not None and folder_name in name_elem.text:
            for ls in folder.findall('.//kml:LineString', ns):
                coords_elem = ls.find('.//kml:coordinates', ns)
                if coords_elem is not None and coords_elem.text:
                    coord_pairs = coords_elem.text.strip().split()
                    for pair in coord_pairs:
                        parts = pair.split(',')
                        if len(parts) >= 2:
                            lon = float(parts[0])
                            lat = float(parts[1])
                            coords.append([lat, lon])
    return coords

def main():
    print(f"Reading KML: {KML_FILE}")
    
    # Extract coordinates
    print("Extracting Michael Current (red line)...")
    michael_coords = extract_coordinates_from_kml(KML_FILE, "The Michael Current")
    print(f"  Found {len(michael_coords)} points")
    
    print("Extracting Mary Current (green line)...")
    mary_coords = extract_coordinates_from_kml(KML_FILE, "The Mary Current")
    print(f"  Found {len(mary_coords)} points")
    
    # Create output directory
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    
    # Save to CSV
    michael_df = pd.DataFrame(michael_coords, columns=['lat', 'lon'])
    michael_output = OUTPUT_DIR / "michael_current_points.csv"
    michael_df.to_csv(michael_output, index=False)
    print(f"Saved: {michael_output}")
    
    mary_df = pd.DataFrame(mary_coords, columns=['lat', 'lon'])
    mary_output = OUTPUT_DIR / "mary_current_points.csv"
    mary_df.to_csv(mary_output, index=False)
    print(f"Saved: {mary_output}")
    
    print("\nDone!")

if __name__ == "__main__":
    main()
