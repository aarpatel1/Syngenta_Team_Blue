# put this into google colab or whatever and change your initialize project to your key in google maps

import ee, geemap

# --- EE init ---
try:
    ee.Initialize()
except Exception:
    ee.Authenticate()
    ee.Initialize(project='careful-striker-472320-j3')

# --- Rajasthan ROI (GAUL L1) ---
gaul = ee.FeatureCollection('FAO/GAUL/2015/level1')
rajasthan = (gaul
             .filter(ee.Filter.eq('ADM0_NAME', 'India'))
             .filter(ee.Filter.eq('ADM1_NAME', 'Rajasthan'))
             .first()
             .geometry())

# -----------------------------
# EVI slope (MOD13Q1) per decade
# -----------------------------
START = '2001-01-01'
END   = '2024-12-31'

# Load EVI + QA
vi = (ee.ImageCollection('MODIS/061/MOD13Q1')
      .filterDate(START, END)
      .filterBounds(rajasthan)
      .select(['EVI','SummaryQA']))

# Mask low-quality obs and apply scale factor (0.0001)
def mask_and_scale(img):
    good = img.select('SummaryQA').lt(2)                 # keep good+marginal
    evi  = img.select('EVI').multiply(0.0001).rename('EVI')
    # keep timestamp so we can compute time
    return evi.updateMask(good).copyProperties(img, ['system:time_start'])

vi_masked = vi.map(mask_and_scale)

# Add time (years since 2000-01-01)
def add_time(img):
    years = ee.Date(img.get('system:time_start')).difference(
        ee.Date('2000-01-01'), 'year'
    )
    return img.addBands(ee.Image.constant(years).rename('t'))

with_time = vi_masked.map(add_time)

# Linear regression per pixel: EVI ~ t
fit = with_time.select(['t','EVI']).reduce(ee.Reducer.linearFit())
evi_slope_decade = fit.select('scale').multiply(10).rename('EVI_slope_decade')  # per decade

# -----------------------------
# Cropland mask (MCD12Q1)
# -----------------------------
year = 2019
modis = (ee.ImageCollection('MODIS/006/MCD12Q1')
         .filterDate(f'{year}-01-01', f'{year}-12-31')
         .first()
         .select('LC_Type1'))

# 12 = Cropland, 14 = Cropland/Natural Veg Mosaic
cropland_mask = modis.remap([12, 14], [1, 1]).selfMask()
cropland_mask_roi = cropland_mask.clip(rajasthan)

# EVI slope on cropland only
evi_slope_cropland_only = evi_slope_decade.updateMask(cropland_mask_roi)

# --- Visualization (red → white → green, centered on 0) ---
evi_viz = {
    'min': -0.05,             # -0.05 EVI / decade
    'max':  0.05,             #  0.05 EVI / decade
    'palette': ['#b2182b','#f7f7f7','#1a9850']  # red → white → green
}
crop_viz = {'min': 0, 'max': 1, 'palette': ['#cdb33b']}

# --- Map (same style as yours) ---
Map = geemap.Map()
Map.centerObject(rajasthan, 6)

Map.addLayer(evi_slope_decade.clip(rajasthan), evi_viz, 'EVI Slope/Decade (All Land)', True)
Map.addLayer(cropland_mask_roi, crop_viz, 'Cropland Mask', False)
Map.addLayer(evi_slope_cropland_only, evi_viz, 'EVI Slope/Decade (Cropland Only)', True)

# Show & save
display(Map)
Map.save('rajasthan_evi_slope.html')
print('Saved: rajasthan_evi_slope.html')
