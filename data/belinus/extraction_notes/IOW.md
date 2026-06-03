# IOW Extraction Notes (Volume 1, Locations 818, 838, and 839 of 2948)

## Maps Overview

Three distinct maps are presented in this section:

1. `area_currents` (818 of 2948)
2. `node_detail` (838 of 2948)
3. `region_overview` (839 of 2948)

---

### 1. `area_currents` (818 of 2948)

*Displays a detailed local map of Brading Isle mapping the Elen and Belinus currents.*

* **The Belinus Current (Gold):** Flows through the southeastern sector of the island.
* **Entry Point:** Bembridge Down (Designated as the *Head of the IOW Serpent*).
* **Path:** Tracks inland through the *Yaverland* node.
* **Nodes Visited (2):** Bembridge Down, Yaverland.


* **The Elen Current (Purple):** Tracks north of the Belinus current across the peninsula.
* **Entry Point:** The Nostril caves at Culver Down.
* **Path:** Heads northwest, cutting through *Bembridge Fort* and continuing onward through *Centurion's Copse*.
* **Nodes Visited (3):** Culver Down (The Nostrils), Bembridge Fort, Centurion's Copse.


* **Auxiliary Nodes:** Bembridge Windmill serves as an auxiliary marker and does not lie on either current.

---

### 2. `node_detail` (838 of 2948)

*Provides localized node and tracking data focusing on the Brading Down area.*

* **The Central Line (Black):** Placed on the left (western) side of the map view. It passes in close proximity to *Bloodstone Spring* before tracking toward *Ashey*.
* **Proximity Threshold:** Passes within 250m of Bloodstone Spring, capturing the local springs and woodland attributed to Eaglehead and Bloodstone Copses.


* **The Elen Current (Purple):** * **Path:** Enters the view via *Bloodstone Spring*, continues along the corridor between Brading Down and Nunwell House, passes directly through the primary node of focus at **Devil's Punchbowl**, and terminates its local run tracking west-to-east into *Brading Church*.
* **The Belinus Current (Gold):** * **Path:** Originates from the bottom of the map view at *Brading Roman Villa* and tracks through *Adgestone Vineyard*. It hits the node of focus at **Devil's Punchbowl** before carrying on toward the northeast without passing any further major landmarks, moving in the definitive direction of *Ryde*.
* **Intersection Points:** The Elen and Belinus currents meet at a single localized node: **Devil's Punchbowl**.

---

### 3. `region_overview` (839 of 2948)

*A macro-level map displaying regional alignments, tracking data across a much broader area, and incorporating a richer set of placemarkers.*

#### **The Central Line (Black)**

Tracks sequentially from South to North across the region. The line passes directly through (**within 250m**): Battery Gardens, Christ Church (within 50m), St Patrick's Church (within 70m), East Ashey Earthworks (within 25m), and Kemphill (within 200m).

> **Anchor Revision Note:** Originally, Battery Gardens was considered the definitive tracking anchor. This was revised to *Widford* following a rigorous canonical-bearing fit analysis (see Section 2.4 of the protocol).

| Near-Miss / Regional Node | Approximate Distance to Central Line | Positional Context |
| --- | --- | --- |
| **Christ Church** | < 50m | Neighboring church with St Patrick's (within 100m) |
| **St Patrick's Church** | < 70m | Neighboring church with Christ Church (within 100m) |
| **East Ashey Earthworks** | < 25m | Medieval settlement 100m SE and 350m NE of East Ashey Manor Farm |
| **Bloodstone Spring** | < 250m | Formally captured via the `node_detail` layout |
| **Kemphill** | < 200m | Farmhouse alignment |
| **Upton** | < 500m | Labeled as *Upton Cross* / *Upton* on the ebook map |
| **Eleanor's Grove** | ~1km | A3054 road sector between Fishbourne Lane and Quarr Abbey |

* **Trajectory Note:** The line is anchored at its southernmost point by a circular plant bed. Beyond Upton, the line carries on northwest over the coast without intersecting any further tight landmarks.

#### **Current Tracking Paths**

* **Elen Current (Purple):** Enters at **Culver Down (The Nostrils caves)** $\rightarrow$ Bembridge Fort $\rightarrow$ Centurion's Copse (Wolverton site) $\rightarrow$ Brading $\rightarrow$ Devil's Punchbowl $\rightarrow$ Nunwell House $\rightarrow$ Bloodstone Spring $\rightarrow$ East Ashey Earthworks $\rightarrow$ Ashey $\rightarrow$ Ruin (12th-century Cistercian Quarr Abbey remains) $\rightarrow$ Quarr Abbey (20th-century Benedictine building) $\rightarrow$ exits beyond the coast.
* **Belinus Current (Gold):** Enters at **Bembridge Down (Head of the IOW Serpent)** $\rightarrow$ Yaverland $\rightarrow$ Brading Roman Fort $\rightarrow$ Devil's Punchbowl $\rightarrow$ Swanmore $\rightarrow$ Ryde $\rightarrow$ Binstead $\rightarrow$ exits beyond the coast.

> **Major Regional Meeting Points:** The **Devil's Punchbowl** serves as the primary regional intersection point where the Elen and Belinus currents converge.

* **Regional Auxiliaries:** Red Cliff and Whitecliff Ledge appear on the map overview but are confirmed as non-entry points. They are retained in the database strictly as auxiliary markers (`is_canonical = FALSE`) for macro completeness.

---

## Map Canonical 33 (Vol 3, Loc 211 Canonical List)

* **Brading Down:** This is the only node from the master 33-list present within this data set.
* **Current Alignment:** Lies on the Elen Current (the mathematically traced path passes roughly 200m northeast of the Brading Down marker).
* **Line Proximity:** Situated approximately 850m away from the black Central Line.