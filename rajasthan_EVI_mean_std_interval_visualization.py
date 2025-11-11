# ------------------------------------------------------------
# Rajasthan EVI 95% Prediction Interval Maps (Separate Panels)
# ------------------------------------------------------------

import pandas as pd
import geopandas as gpd
import matplotlib.pyplot as plt
import json
from shapely.geometry import Point

# ============================================================
# 1. Load and prepare data
# ============================================================

csv_path = "Rajasthan_EVI_MeanStd_95PI_Sample.csv"
df = pd.read_csv(csv_path)

def parse_point(geo_str):
    try:
        coords = json.loads(geo_str)["coordinates"]
        return Point(coords)
    except:
        return None

df["geometry"] = df[".geo"].apply(parse_point)
gdf = gpd.GeoDataFrame(df, geometry="geometry", crs="EPSG:4326")

# ============================================================
# 2. Compute derived values
# ============================================================

gdf["PI_width"] = gdf["Upper_95"] - gdf["Lower_95"]

# ============================================================
# 3. Map 1 — Prediction Interval Width
# ============================================================

fig, ax = plt.subplots(figsize=(8, 10))
gdf.plot(column="PI_width", cmap="viridis", legend=True,
         legend_kwds={"label": "PI width (EVI units)"}, ax=ax, markersize=5)
ax.set_title("Pixel-level EVI 95% Prediction Interval Width")
ax.set_xlabel("Longitude")
ax.set_ylabel("Latitude")
plt.tight_layout()
plt.savefig("EVI_95PI_Width.png", dpi=300)
plt.show()

# ============================================================
# 4. Map 2 — Lower Tail (Lower_95)
# ============================================================

fig, ax = plt.subplots(figsize=(8, 10))
gdf.plot(column="Lower_95", cmap="Blues", legend=True,
         legend_kwds={"label": "Lower tail cutoff (EVI)"}, ax=ax, markersize=5)
ax.set_title("Pixel lower tail (below 95% PI)")
ax.set_xlabel("Longitude")
ax.set_ylabel("Latitude")
plt.tight_layout()
plt.savefig("EVI_95PI_LowerTail.png", dpi=300)
plt.show()

# ============================================================
# 5. Map 3 — Upper Tail (Upper_95)
# ============================================================

fig, ax = plt.subplots(figsize=(8, 10))
gdf.plot(column="Upper_95", cmap="Reds", legend=True,
         legend_kwds={"label": "Upper tail cutoff (EVI)"}, ax=ax, markersize=5)
ax.set_title("Pixel upper tail (above 95% PI)")
ax.set_xlabel("Longitude")
ax.set_ylabel("Latitude")
plt.tight_layout()
plt.savefig("EVI_95PI_UpperTail.png", dpi=300)
plt.show()

print("✅ Generated 3 maps:")
print(" - EVI_95PI_Width.png")
print(" - EVI_95PI_LowerTail.png")
print(" - EVI_95PI_UpperTail.png")
