import pandas as pd
import matplotlib.pyplot as plt
from mpl_toolkits.basemap import Basemap
import numpy as np
from scipy.interpolate import griddata

# Load and clean data
df = pd.read_csv("SlopeValues_Jaipur_AOI_1km.csv")
df['latitude'] = pd.to_numeric(df['latitude'], errors='coerce')
df['longitude'] = pd.to_numeric(df['longitude'], errors='coerce')
df = df.dropna(subset=['latitude', 'longitude'])

# Compute center and extent
lat_min, lat_max = df['latitude'].min(), df['latitude'].max()
lon_min, lon_max = df['longitude'].min(), df['longitude'].max()
lat_center = (lat_min + lat_max) / 2
lon_center = (lon_min + lon_max) / 2

# Large zoom-out for wide view
zoom_out_factor = 5.0
lat_half_range = (lat_max - lat_min) * zoom_out_factor / 2
lon_half_range = (lon_max - lon_min) * zoom_out_factor / 2
lat_min = lat_center - lat_half_range
lat_max = lat_center + lat_half_range
lon_min = lon_center - lon_half_range
lon_max = lon_center + lon_half_range

# Create map
plt.figure(figsize=(12, 10))
m = Basemap(projection='cyl',
            llcrnrlat=lat_min, urcrnrlat=lat_max,
            llcrnrlon=lon_min, urcrnrlon=lon_max,
            resolution='i')

m.drawcountries()
m.drawstates()
m.drawmapboundary(fill_color='beige')
m.fillcontinents(color='cornsilk', lake_color='beige')

# Convert coordinates
x, y = m(df['longitude'].values, df['latitude'].values)

# Interpolate slope data to fill entire map area
numcols, numrows = 500, 500
xi = np.linspace(lon_min, lon_max, numcols)
yi = np.linspace(lat_min, lat_max, numrows)
xi, yi = np.meshgrid(xi, yi)

# Linear interpolation inside convex hull
zi_linear = griddata((df['longitude'], df['latitude']),
                     df['slope_per_year'], (xi, yi), method='linear')

# Extrapolate outside convex hull with nearest neighbor
zi_nearest = griddata((df['longitude'], df['latitude']),
                      df['slope_per_year'], (xi, yi), method='nearest')

# Combine: fill NaNs with nearest values
zi_filled = np.where(np.isnan(zi_linear), zi_nearest, zi_linear)

# Plot scatter points
sc = m.scatter(x, y, c=df['slope_per_year'], cmap='coolwarm',
               s=70, edgecolors='black', alpha=0.9, zorder=5)

# Draw contour lines ONLY (covering full map)
levels = np.linspace(df['slope_per_year'].min(),
                     df['slope_per_year'].max(), 14)
cs = m.contour(xi, yi, zi_filled, levels=levels,
               cmap='coolwarm', linewidths=1.2, alpha=0.9, zorder=6)
plt.clabel(cs, inline=True, fontsize=8, fmt="%.2f")

# Add colorbar for slope reference
cbar = plt.colorbar(sc, orientation='vertical', shrink=0.7, pad=0.05)
cbar.set_label("Slope per Year")

plt.title("Extended Contour Lines Across Map (No Fill - Jaipur Region)")
plt.show()
