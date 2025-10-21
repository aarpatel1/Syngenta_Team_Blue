# 🌿 EVI Slope Mapping with Folium and OpenStreetMap

## 🧭 Overview
This project visualizes **Enhanced Vegetation Index (EVI) slope trends** over time using **OpenStreetMap (OSM)** as the base layer.  
Each pixel in the CSV represents a geospatial point with a calculated slope value (change in EVI per decade).  
Colors indicate the trend:

- 🟥 **Red** → Negative slope (vegetation decline)  
- ⚪ **White** → Neutral / Stable vegetation  
- 🟩 **Green** → Positive slope (vegetation growth)

The resulting map is interactive, allowing you to explore slope trends geographically.

---

## 📁 Project Structure

evi_map_project/
│
├── slope_values.csv # Exported data from Google Earth Engine
├── map_evi.py # Python script that generates the map
├── evi_slope_map.html # Output interactive map (auto-generated)
└── README.md # This file


---

## 🧱 Setup Instructions

### 1️⃣ Create and activate a virtual environment

**Windows (PowerShell / CMD):**
```bash
python -m venv .venv
.venv\Scripts\activate

macOS / Linux:

python3 -m venv .venv
source .venv/bin/activate

2️⃣ Install dependencies

pip install folium pandas branca

3️⃣ Place your CSV file

Ensure your CSV file (with columns like latitude, longitude, slope_per_decade) is in the same directory as the script.
4️⃣ Run the script

python map_evi.py

This will generate an interactive map file named evi_slope_map.html in the same directory.
5️⃣ View the map

Open the generated HTML file in your web browser:

start evi_slope_map.html      # Windows
open evi_slope_map.html       # macOS
xdg-open evi_slope_map.html   # Linux

🗺️ Visualization Example

    Base map: OpenStreetMap tiles

    Color scale: Red → White → Green (decline to growth)

    Popups: Show latitude, longitude, and slope value for each pixel

🧩 Customization

You can adjust visualization options in map_evi.py:

    Change color gradient in the LinearColormap definition

    Adjust marker size or opacity

    Replace points with a heatmap or continuous raster layer

🧠 Next Steps

    Create a smoothed raster mask overlay for a continuous color field

    Use Kepler.gl or Leafmap for 3D visualization

    Integrate with Google Earth Engine exports for real-time updates