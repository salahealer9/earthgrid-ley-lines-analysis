#!/usr/bin/env python3
"""
Convert a KML LineString to a CSV vertex file matching the Belinus schema.
Per Section 6.7 of POPULATION_CORRIDOR_PROTOCOL_BELINUS.md.
"""

import csv
import sys
import xml.etree.ElementTree as ET

def kml_to_csv(kml_file, output_csv, map_name):
    """
    Extract coordinates from a KML LineString and write to CSV.
    
    Args:
        kml_file: path to input KML file
        output_csv: path to output CSV file
        map_name: name of the map (e.g., "IOW_Overview")
    """
    ns = {'kml': 'http://www.opengis.net/kml/2.2'}
    tree = ET.parse(kml_file)
    root = tree.getroot()
    
    # Find the first LineString
    line_string = root.find('.//kml:LineString', ns)
    if line_string is None:
        print("Error: No LineString found in KML")
        return
    
    coords_elem = line_string.find('kml:coordinates', ns)
    if coords_elem is None or not coords_elem.text:
        print("Error: No coordinates found")
        return
    
    # Parse coordinates
    coord_pairs = coords_elem.text.strip().split()
    vertices = []
    for i, pair in enumerate(coord_pairs):
        parts = pair.split(',')
        if len(parts) >= 2:
            lon = float(parts[0])
            lat = float(parts[1])
            vertices.append({
                'map_name': map_name,
                'vertex_index': i,
                'lat': lat,
                'lon': lon,
                'vertex_type': 'generic',
                'name': '',
                'notes': ''
            })
    
    # Write CSV
    with open(output_csv, 'w', newline='') as f:
        writer = csv.DictWriter(f, fieldnames=['map_name', 'vertex_index', 'lat', 'lon', 'vertex_type', 'name', 'notes'])
        writer.writeheader()
        writer.writerows(vertices)
    
    print(f"Converted {len(vertices)} vertices from {kml_file} to {output_csv}")

if __name__ == "__main__":
    if len(sys.argv) != 4:
        print("Usage: python scripts/kml_to_csv.py <kml_file> <output_csv> <map_name>")
        sys.exit(1)
    
    kml_to_csv(sys.argv[1], sys.argv[2], sys.argv[3])