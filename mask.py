import pandas as pd
import folium
import branca.colormap as cm

# Load the CSV
df = pd.read_csv("slope_values.csv")

# Center the map
center_lat, center_lon = df["latitude"].mean(), df["longitude"].mean()

# Create the OpenStreetMap base
m = folium.Map(location=[center_lat, center_lon], zoom_start=14, tiles="OpenStreetMap")

# Define a diverging color map: red → white → green
min_val, max_val = df["slope_per_decade"].min(), df["slope_per_decade"].max()
colormap = cm.LinearColormap(
    colors=['red', 'white', 'green'],
    vmin=min_val,
    vmax=max_val
).to_step(20)  # smooth 20-step gradient
colormap.caption = 'EVI Slope per Decade (Red = decline, Green = growth)'

# Add each pixel as a colored circle
for _, row in df.iterrows():
    slope = row["slope_per_decade"]
    folium.CircleMarker(
        location=[row["latitude"], row["longitude"]],
        radius=6,
        color=colormap(slope),
        fill=True,
        fill_color=colormap(slope),
        fill_opacity=0.85,
        popup=folium.Popup(
            f"<b>Lat:</b> {row['latitude']:.6f}<br>"
            f"<b>Lon:</b> {row['longitude']:.6f}<br>"
            f"<b>Slope per decade:</b> {slope:.3f}",
            max_width=200
        ),
    ).add_to(m)

# Add the legend
colormap.add_to(m)

# Save or display
m.save("evi_slope_map.html")
m
