# South Hampshire Extraction Notes (Volume 1, Location 1008, 1146 and 1147 of 2948)

## Maps

Three maps are presented: `area_currents` (1008 of 2948), `node_detail` (1146 of 2948) and `region_overview` (1147 of 2948).

### `area_currents` (1008 of 2948)

- Displays a map of Titchfield showing the central line, as well as the Elen and Belinus currents.
- The central line does not have a precise node of its own but passes very close to several nodes.
- From south to north, the entry point of the Belinus current is defined as **St Peter's Church**, passing through the canal and the Meon River from the south-east.
- The Belinus current passes through the node Bugle at "The Square (Site of the Old Market Hall)" before continuing along High Street close to the black central line. Beyond East Street, the Belinus current follows the central black line closely to pass through the node Tithe Barn (~150m), then curves in an approximate quarter-circle from south to east to pass through Titchfield Abbey. The Belinus current exits through the ponds of the Abbey towards the north.
- The Belinus current passes through four nodes: St Peter's Church, Bugle, Tithe Barn, and Titchfield Abbey.
- From south to north, the entry point of the Elen current is **Great Posbrook Farm**. Continuing north-east, it passes through St Peter's Church, then continues north along the canal and the Meon River to pass through Old Corn Mill (currently called the Titchfield Mill). Continuing north along the canal and the Meon River, the Elen current then turns left, passing through Anjou Bridge before exiting Titchfield Abbey to the north-west, gradually approaching the black central line.
- The Elen current passes through four nodes: Great Posbrook Farm, St Peter's Church, Old Corn Mill (now called The Titchfield Mill), and Titchfield Abbey.
- The two meeting points of the currents are the nodes St Peter's Church and Titchfield Abbey.
- The nodes Sarsen Stones, St Margaret's Priory, Site of Shakespeare's School, and Fisherman's Rest are auxiliary and are not nodes of any current.

### `node_detail` (1146 of 2948)

- Node detail for St Catherine's Hill.
- Shows the Belinus alignment (grey central line), which passes through the Labyrinth node on St Catherine's Hill.
- Two currents meet at the "Trees" node, centered in the Inner Sanctum, and at the "Labyrinth" node.
- The purple Elen current passes through the "Trees" node at the Inner Sanctum and the center of the "Labyrinth" node.
- The gold Belinus current passes through the "Trees" node at the Inner Sanctum and the center of the "Labyrinth" node.

### `region_overview` (1147 of 2948)

A much richer map showing many more placemarkers.

**Central line (black):** Passes through Titchfield St Peter's Church, Roman Fort Curbridge, Marwell Manor, St Catherine's Hill and Winchester Cathedral. All of them well within 250 m.

The black central line passes near:

- Hill Head ~550m
- Titchfield Abbey ~500m (as seen in `area_currents`)
- Twyford St Mary's Church ~950m
- St Cross Church ~800m
- Botley (All Saints Church) ~650m
- Great Posbrook Farm ~650m
- Crofton Old Church ~650m

**Elen current (purple):** Enters at **Meon** (through the Meon Spit), then passes through:
- Great Posbrook Farm
- Titchfield St Peter's Church
- Titchfield Abbey
- Roman Fort Curbridge
- Botley
- Bishopstoke Old Church
- Otterbourne Manor
- Twyford
- St Cross

**Belinus current (gold):** Enters at **Alverstoke Motte** (through Browndown), then passes through:
- Crofton Old Church
- Titchfield St Peter's Church
- Titchfield Abbey
- Wickham
- Shedfield
- Bishops Waltham (Eastern and Western nodes)
- St Catherine's Hill
- Morestead

- **Winchester Cathedral**, **St Catherine's Hill**, **St Peter's Church** and **Titchfield Abbey** are meeting points of Elen and Belinus currents.

- **Auxiliary:** Meon Spit, Browndown, Gosport and Fareham

### Bishop's Waltham nodes

Biltcliffe's text explicitly mentions the **ruins of the Palace of the Bishops of Winchester** as the eastern node on the Belinus current. The map shows two nodes labelled "Bishop's Waltham":

- **Eastern Node**: the historic Palace of the Bishops of Winchester (explicitly mentioned in text)
- **Western Node**: the geologically significant Claylands area (shown on map; not mentioned in text)

Both are treated as canonical nodes (`is_canonical = TRUE`) because they appear as marked nodes on the map.

### Central line inconsistency (Titchfield area)

The overview map and the area currents map show the central line in different positions:

- Overview map: if traced from Hill Head northward, the line passes through Great Posbrook Farm.
- Area currents map: the line passes through St Peter's Church square.

The two maps are inconsistent by approximately 650m if we trace from Hill Head. The traced central line follows the **area currents map** for this segment, placing the line through St Peter's Church square. This choice prioritises the local detail map over the overview map for this node.

Consequence: the line is offset from Hill Head by approximately 650m compared to the overview map path.

This discrepancy is noted but does not affect the statistical tests, which use the mathematically defined great circle (Widford + bearing) as the canonical line.