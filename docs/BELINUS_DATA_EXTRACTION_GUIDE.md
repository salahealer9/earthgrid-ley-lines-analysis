# Belinus Line Data Extraction Guide

This document records the workflow and conventions used to extract geometric data from Biltcliffe and Hoare's *The Spine of Albion* (2012, revised ePub edition) for the Belinus Line case study.

**Provenance note**: All counts and node lists below are derived from manual identification on Biltcliffe and Hoare (2012); they are cross-references to the source's published claims, not reproductions of the source's traced map geometry.

## 1. Overview

The extraction process converts manually traced paths from the eBook maps into structured CSV files following the schema defined in `POPULATION_CORRIDOR_PROTOCOL_BELINUS.md`.

Three geometric features are traced for each map:

| Feature | File | Description |
|---------|------|-------------|
| Central line | `central_line_vertices.csv` | Straight alignment traced from the eBook map (bearing approximately 345.5°). Nodes within ~250 m are recorded in `nodes.csv` with `on_central_line = TRUE`. |
| Belinus current | `belinus_current_vertices.csv` | Male meandering current (orange/gold on Biltcliffe's maps). |
| Elen current | `elen_current_vertices.csv` | Female meandering current (purple on Biltcliffe's maps). |

## 2. Tracing Workflow

### 2.1 Tools

- **Google Earth Pro** (free desktop version): used for tracing paths from eBook map overlays
- **Python script** `scripts/kml_to_csv.py`: converts KML LineStrings to CSV vertices

### 2.2 Tracing Procedure

1. Open the eBook map in Google Earth Pro as an image overlay.
2. Georeference the overlay by aligning known landmarks (coastline, major roads, towns) with satellite imagery.
3. Use the **"Add Path"** tool to trace the feature:
   - Click at intervals of approximately 200–500 m to capture meander shapes.
   - At named nodes (from `nodes.csv`), place vertices at the exact coordinates from `nodes.csv`.
4. Save each traced feature as a separate KML file.
5. Convert KML to CSV using `kml_to_csv.py`.

### 2.3 Running `kml_to_csv.py`

```bash
python scripts/kml_to_csv.py <input.kml> <output.csv> <map_name>
```

**Arguments:**

| Argument | Description | Example |
|----------|-------------|---------|
| `input.kml` | KML file containing a single LineString | `elen_current_IOW.kml` |
| `output.csv` | Output CSV file | `data/belinus/elen_current_vertices.csv` |
| `map_name` | Name of the map (matches `map_metadata.csv`) | `IOW_Overview` |

**Example:**

```bash
python scripts/kml_to_csv.py \
  data/belinus/kml/elen_current_IOW.kml \
  data/belinus/elen_current_vertices.csv \
  IOW_Overview
```

### 2.4 Post‑Processing

After conversion, edit the CSV to:

- Set `vertex_type`:
  - `endpoint` for the first and last vertex of the path on a given map
  - `node` for vertices that coincide with named nodes (from `nodes.csv`)
  - `crossing` where a current crosses the central line (if applicable)
  - `generic` for all other vertices
- Fill the `name` column for `node` vertices (exact spelling as in `nodes.csv`)
- Add `notes` as needed (e.g., "continues off map", "crosses central line")

Coordinates of `node` vertices are replaced with the exact values from `nodes.csv` (not the traced approximation).

## 3. Vertex Counts (Isle of Wight Overview Map)

| Feature | Vertices | Nodes in vertices | File |
|---------|----------|-------------------|------|
| Central line | 26 | 0 (nodes recorded separately in `nodes.csv`) | `central_line_vertices.csv` (local only) |
| Belinus current | 50 | 7 | `belinus_current_vertices.csv` (local only) |
| Elen current | 99 | 11 | `elen_current_vertices.csv` (local only) |

**Total vertices traced: 175**

## 4. Google Earth Styling for Placemarks

*This section documents the analyst's working setup; the colours have no analytical significance — they are visual aids for the tracing workflow.*

### 4.1 Colour Scheme

| Category | Colour | Hex | KML (AABBGGRR) |
|----------|--------|-----|----------------|
| Central line node | Red | `#ef5350` | `FF5053EF` |
| Belinus current node | Gold | `#fbc02d` | `FF2DC0FB` |
| Elen current node | Purple | `#ab47bc` | `FFBC47AB` |
| Near central line (within ~250 m) | Orange | `#ffa726` | `FF26A7FF` |
| Auxiliary node | Blue | `#0000ff` | `FFFF0000` |
| Meeting point (two currents) | Magenta (star icon) | `#ff00ff` | `FFFF00FF` |

### 4.2 Setting Colours in Google Earth Pro

1. Right‑click the placemark → **Properties** (or **Get Info**).
2. Click the colour square next to the name.
3. Choose a colour from the palette, or enter a custom hex code:
   - Click the **rainbow wheel** or **"Custom"** tab.
   - Enter the hex code (e.g., `#fbc02d` for gold).
4. Click **OK**.

### 4.3 Setting Icons

- For the **meeting point** (Devil's Punchbowl), use a **star** icon.
- For all other nodes, use the **default circle** icon.

### 4.4 Batch Colour Editing via KML

To apply colours to many placemarks at once:

1. Export placemarks as KML.
2. Open the KML in a text editor.
3. Find `<color>` tags and replace the hex values (KML uses `AABBGGRR` format).
4. Re‑import the KML into Google Earth.

**KML colour examples:**

| Colour | HTML hex | KML (AABBGGRR) |
|--------|----------|----------------|
| Red | `#ef5350` | `FF5053EF` |
| Gold | `#fbc02d` | `FF2DC0FB` |
| Purple | `#ab47bc` | `FFBC47AB` |
| Orange | `#ffa726` | `FF26A7FF` |
| Blue | `#0000ff` | `FFFF0000` |
| Magenta | `#ff00ff` | `FFFF00FF` |

## 5. Folder Structure in Google Earth

```
Belinus Line - Isle of Wight
│
├── 📁 Central Line (Red #ef5350)
│   Description: Nodes exactly on or within ~250 m of the straight central alignment (traced from eBook map, bearing ~345.5°)
│
├── 📁 Belinus Current (Gold #fbc02d)
│   Description: Nodes on the male meandering current (gold on Biltcliffe's map)
│
├── 📁 Elen Current (Purple #ab47bc)
│   Description: Nodes on the female meandering current (purple on Biltcliffe's map)
│
├── 📁 Near Central Line (Orange #ffa726)
│   Description: Nodes within ~250 m of the central line but not on any current
│
└── 📁 Auxiliary (Blue #0000ff)
    Description: Named places not on any feature (informational only)
```

## 6. Map Metadata (Isle of Wight)

### IOW_Overview (region overview)

```csv
IOW_Overview,region_overview,Southern England,1,839,345.5,TRUE,TRUE,TRUE,24,26,99,50,"Region overview map of the Isle of Wight. Approximated central line traced from eBook map; vertices every 200–500m; Central line passes through Battery Gardens, Christ Church, St Patrick's Church, Bloodstone Spring (within 250 m), East Ashey Earthworks (within 250 m), Kemphill (within 250 m). Elen current (purple) passes through Culver Down, Bembridge Fort, Centurion's Copse, Brading, Devil's Punchbowl (meeting point), Nunwell House, Bloodstone Spring, East Ashey Earthworks, Ashey, Ruin (medieval abbey ruins), Quarr Abbey. Belinus current (gold) passes through Yaverland, Brading Roman Fort, Devil's Punchbowl (meeting point), Swanmore, Ryde, Binstead. The two currents meet at Devil's Punchbowl."
```

### IOW_Detail_Bloodstone (node detail)

```csv
IOW_Detail_Bloodstone,node_detail,Southern England,1,838,345.5,TRUE,TRUE,TRUE,5,0,4,2,"Node detail map centred on Bloodstone Spring. Central line is shown (black) passing near Bloodstone Spring to Ashey. Elen current (purple) passes through Bloodstone Spring, Brading Down, Nunwell House, Devil's Punchbowl, Brading Church. Belinus current (gold) passes through Brading Roman Villa, Adgestone Vineyard, Devil's Punchbowl, then northeast towards Ryde. Devil's Punchbowl is the meeting point of the two currents."
```

## 7. Node Count Summary (Isle of Wight)

| Category | Nodes |
|----------|-------|
| Central line | 4 (Battery Gardens, Christ Church, St Patrick's Church, Kemphill) |
| Belinus current | 7 (Yaverland, Red Cliff, Brading Roman Fort, Devil's Punchbowl, Ryde, Swanmore, Binstead) |
| Elen current | 11 (Bloodstone Spring, East Ashey Earthworks, Ashey, Whitecliff Ledge, Quarr Abbey, Ruin, Culver Down, Bembridge Fort, Centurions Copse, Brading, Nunwell House) |
| Near central line | 1 (Upton) |
| Auxiliary | 1 (Eleanor's Grove) |
| **Total** | **24** |

## 8. Copyright and Data Availability

Per Section 13 of the pre‑registered protocol (`POPULATION_CORRIDOR_PROTOCOL_BELINUS.md`), traced vertex files (`central_line_vertices.csv`, `elen_current_vertices.csv`, `belinus_current_vertices.csv`) are **not** included in the public Zenodo deposit by default. They are kept local to the analyst's machine.

Coordinates of named places (`nodes.csv`) are factual geographic data and are published under CC‑BY‑4.0.

## 9. Version History

| Date | Change |
|------|--------|
| 2026-05-26 | Initial version; IOW extraction complete (24 nodes, 175 vertices across three traced features). |
```
