# Spatial Relationship Mapper QGIS Plugin

![Plugin Icon](https://github.com/AnustupJana/SpatialRelationshipMapper-plugin/blob/main/icon.png?raw=true)

## Overview
The **Spatial Relationship Mapper** plugin for QGIS allows users to create spatial relationships between two polygon layers with ease. It identifies intersecting features and links their attribute IDs in both layers.

This tool is useful for workflows like:
- Parcel ↔ Building mapping
- Land use ↔ Structures
- Zone ↔ Assets relationships

---

## Features
✔ Select any two polygon layers  
✔ Choose custom ID fields from both layers  
✔ Automatically detects spatial intersections  
✔ Outputs:
- Layer 1 with related Layer 2 IDs  
- Layer 2 with related Layer 1 IDs  
✔ Supports both temporary and saved outputs  
✔ Fast processing using spatial indexing  

---

## How It Works
1. Select **Layer 1 (Parcel or any polygon layer)**  
2. Select its **ID field**  
3. Select **Layer 2 (Building or any polygon layer)**  
4. Select its **ID field**  
5. Run the tool  

The plugin will:
- Detect intersecting features  
- Create relationship mapping  
- Add a new field (`related_ids`) in both outputs  

---

## Installation
1. Download or clone this repository  
2. Copy the folder: spatial_relationship_mapper
3. Paste into your QGIS plugin directory: C:\Users<YourUser>\AppData\Roaming\QGIS\QGIS3\profiles\default\python\plugins
4. Restart QGIS  
5. Enable plugin from: Plugins → Manage and Install Plugins

---

## Usage
- Open: Processing Toolbox → Spatial Analysis Tools → Spatial Relationship Mapper
- Or use toolbar icon after enabling plugin  

---

## Output
- **Layer 1 Output** → contains related Layer 2 IDs  
- **Layer 2 Output** → contains related Layer 1 IDs  
- Relationship stored in: related_ids (string, pipe-separated)

---

## Example
Parcel ID: `P101`  
Building IDs: `B12 | B15 | B18`  

---

## Requirements
- QGIS 3.16 or later  

---

## Author
**Anustup Jana**  
📧 anustupjana21@email.com  

---

## License
This project is licensed under the MIT License - see the [LICENSE](https://github.com/AnustupJana/SpatialRelationshipMapper-plugin/blob/main/LICENSE) file for details.

---

## Support
If you find this plugin useful, feel free to ⭐ the repository and share feedback!
