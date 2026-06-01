# South Hampshire Extraction Notes (Volume 1, Locations 1008, 1146, and 1147 of 2948)

## Maps Overview

Three distinct maps are presented in this section:

1. `area_currents` (1008 of 2948)
2. `node_detail` (1146 of 2948)
3. `region_overview` (1147 of 2948)
4. `area_currents` (1567 of 2948)

---

### 1. `area_currents` (1008 of 2948)

*Displays a detailed map of Titchfield mapping the Central Line, the Belinus Current, and the Elen Current.*

* **The Central Line (Black):** Does not feature a precise node of its own in this view, but passes in close proximity to several local nodes.
* **The Belinus Current (Gold):** Enters from the southeast, flowing South to North along the canal and the Meon River.
* **Entry Point:** St. Peter's Church
* **Path:** Passes through the *Bugle* node at "The Square (Site of the Old Market Hall)", runs north along High Street close to the Central Line, and continues past East Street. It then passes through the *Tithe Barn* node (~150m) before curving in an approximate quarter-circle from south to east to hit *Titchfield Abbey*, exiting via the Abbey ponds toward the north.
* **Nodes Visited (4):** St. Peter's Church, Bugle, Tithe Barn, Titchfield Abbey.


* **The Elen Current (Purple):** Flows South to North, gradually converging toward the Central Line.
* **Entry Point:** Great Posbrook Farm
* **Path:** Heads northeast through *St. Peter's Church*, follows the canal and Meon River north to pass through *Old Corn Mill* (currently named The Titchfield Mill), continues north along the river, turns left through *Anjou Bridge*, and exits *Titchfield Abbey* to the northwest.
* **Nodes Visited (4):** Great Posbrook Farm, St. Peter's Church, Old Corn Mill (The Titchfield Mill), Titchfield Abbey.


* **Intersection Points:** The two currents meet at **St. Peter's Church** and **Titchfield Abbey**.
* **Auxiliary Nodes:** Sarsen Stones, St. Margaret's Priory, Site of Shakespeare's School, and Fisherman's Rest are auxiliary markers and do not lie on either current.

---

### 2. `node_detail` (1146 of 2948)

*Provides localized node data for St. Catherine's Hill.*

* **Belinus Alignment:** The grey central line alignment passes directly through the *Labyrinth* node on St. Catherine's Hill.
* **Current Intersections:** The purple Elen current and gold Belinus current intersect at two specific nodes in this view:
1. The **Trees** node (centered within the Inner Sanctum).
2. The **Labyrinth** node (at its exact center).


---

### 3. `region_overview` (1147 of 2948)

*A macro-level map displaying regional alignments, tracking data across a much broader area.*

#### **The Central Line (Black)**

Passes directly through (**within 250m**): Titchfield St. Peter's Church, Roman Fort Curbridge, Marwell Manor, St. Catherine's Hill, and Winchester Cathedral.

| Near-Miss Node | Approximate Distance to Central Line |
| --- | --- |
| Hill Head | ~550m |
| Titchfield Abbey | ~500m *(as confirmed in area_currents)* |
| Great Posbrook Farm | ~650m |
| Crofton Old Church | ~650m |
| Botley (All Saints Church) | ~650m |
| St. Cross Church | ~800m |
| Twyford St. Mary's Church | ~950m |

#### **Current Tracking Paths**

* **Elen Current (Purple):** Enters at **Meon** (via Meon Spit) $\rightarrow$ Great Posbrook Farm $\rightarrow$ Titchfield St. Peter's Church $\rightarrow$ Titchfield Abbey $\rightarrow$ Roman Fort Curbridge $\rightarrow$ Botley $\rightarrow$ Bishopstoke Old Church $\rightarrow$ Otterbourne Manor $\rightarrow$ Twyford $\rightarrow$ St. Cross.
* **Belinus Current (Gold):** Enters at **Alverstoke Motte** (via Browndown) $\rightarrow$ Crofton Old Church $\rightarrow$ Titchfield St. Peter's Church $\rightarrow$ Titchfield Abbey $\rightarrow$ Wickham $\rightarrow$ Shedfield $\rightarrow$ Bishop's Waltham (Eastern & Western nodes) $\rightarrow$ St. Catherine's Hill $\rightarrow$ Morestead.

> **Major Regional Meeting Points:** Winchester Cathedral, St. Catherine's Hill, St. Peter's Church, and Titchfield Abbey serve as major intersections where the Elen and Belinus currents meet.

* **Regional Auxiliaries:** Meon Spit, Browndown, Gosport, and Fareham.

---

## Analytical Notes & Discrepancies

### Bishop's Waltham Nodes

While Biltcliffe's written text explicitly names only the **ruins of the Palace of the Bishops of Winchester** (the Eastern Node) regarding the Belinus current, the overview map marks two distinct points.

* **Eastern Node:** The historic Palace of the Bishops of Winchester (Supported by text & map).
* **Western Node:** The geologically significant Claylands area (Supported by map only).

**Database Status:** Both are cataloged as canonical nodes (`is_canonical = TRUE`) because both are explicitly designated as markers on the source map.

### Central Line Inconsistency (Titchfield Area)

A physical layout conflict exists between the macro-scale overview map and the micro-scale area currents map:

* **Overview Map:** Traced north from Hill Head, the line is drawn passing through *Great Posbrook Farm*.
* **Area Currents Map:** The line is drawn passing through *St. Peter's Church square*.

**Resolution:** This tracking prioritizes the high-detail **`area_currents` map** for this specific segment, routing the line through St. Peter's Church square. Consequently, the actual mapped line is offset from Hill Head by roughly 650m compared to the overview map's trajectory.

> **Statistical Impact:** This visual discrepancy is noted for mapping fidelity but does not disrupt statistical data testing. Statistical models strictly utilize the mathematically calculated great circle (Widford + bearing) as the definitive canonical line.

---

### 4. `area_currents` (1567 of 2948)

*Displays a detailed local map of Winchester mapping the Central Line, the Belinus Current, and the Elen Current.*

* **The Central Line (Black):** Originating from the south, it tracks sequentially from South to North through the following nodes:
* School House $\rightarrow$ Winchester College $\rightarrow$ Cheyney Court $\rightarrow$ St. Swithun's Gate $\rightarrow$ Former Visitor Centre (3 Symonds Street) $\rightarrow$ St. Lawrence's Church $\rightarrow$ Winchester City Museum $\rightarrow$ The Arc Winchester (Library) $\rightarrow$ Theatre Royal.


* **The Belinus Current (Gold):** Flows South to North, originating at St. Catherine's Hill and exiting toward Flowerdown Barrow.
* **Entry Point:** Wolvesey Castle (ruin)
* **Path:** Winchester Cathedral $\rightarrow$ Former Visitor Centre $\rightarrow$ Former St. Thomas Church $\rightarrow$ Peninsula Barracks $\rightarrow$ Great Hall & Round Table $\rightarrow$ Westgate Museum $\rightarrow$ West Gate $\rightarrow$ Hyde Gate $\rightarrow$ St. Bartholomew's Church.


* **The Elen Current (Purple):** Flows South to North, originating at St. Catherine's Hill and exiting toward Headbourne Worthy.
* **Entry Point:** The Chantry
* **Path:** Winchester College $\rightarrow$ Pilgrims' School $\rightarrow$ Winchester Cathedral $\rightarrow$ Tower of St. Maurice $\rightarrow$ The Brooks Shopping Centre $\rightarrow$ Hyde Abbey.


* **Intersection Point:** The Elen and Belinus currents intersect at a single node: **Winchester Cathedral**.
* **Auxiliary Nodes:** The Leisure Centre, Guildhall, and Barracks Museums are auxiliary markers and do not lie on any current or line.

---

## Analytical Notes & Discrepancies (Winchester Area)

### Map Discrepancies (vs. Gary's Map)

Two distinct placement differences exist when comparing this layout to Gary's original tracking map:

* **Barracks Museums:** The current data places this node in a different position than indicated on Gary's map.
* **Visitor Centre:** The current data does not match the spatial positioning found on Gary's map.



