// ===================================================================
// RAJASTHAN MULTI-YEAR EVI ANALYSIS (2010–2024)
// Author: Aarav Patel (Purdue University / Syngenta Data Mine)
// ===================================================================

// 1️⃣ Load India states and filter for Rajasthan
var states = ee.FeatureCollection("FAO/GAUL/2015/level1");
var rajasthan = states.filter(ee.Filter.eq('ADM1_NAME', 'Rajasthan'));
Map.centerObject(rajasthan, 6);
Map.addLayer(rajasthan, {color: 'blue'}, 'Rajasthan Boundary');

// 2️⃣ Load MODIS MOD13Q1 EVI dataset (16-day composite, 250m)
var eviCollection = ee.ImageCollection('MODIS/006/MOD13Q1')
                      .select('EVI')
                      .filterDate('2010-01-01', '2024-12-31')
                      .filterBounds(rajasthan);

// 3️⃣ Compute mean EVI per year (optional visualization)
var years = ee.List.sequence(2010, 2024);
var yearlyEVI = ee.ImageCollection(
  years.map(function(y) {
    var start = ee.Date.fromYMD(y, 1, 1);
    var end = start.advance(1, 'year');
    var yearMean = eviCollection.filterDate(start, end).mean();
    return yearMean.set('year', y);
  })
);

// 4️⃣ Compute overall mean EVI across all years
var multiYearMeanEVI = yearlyEVI.mean().clip(rajasthan);

// 5️⃣ Visualization parameters
var eviVis = {
  min: 1500,
  max: 7000,
  palette: ['red', 'orange', 'yellow', 'lightgreen', 'green']
};


// 6️⃣ Add mean EVI layer to map
Map.addLayer(multiYearMeanEVI, eviVis, 'Mean EVI (2010–2024)');

// 7️⃣ Optional: Terrain slope overlay for elevation gradient
var dem = ee.Image("USGS/SRTMGL1_003").clip(rajasthan);
var slope = ee.Terrain.slope(dem);
Map.addLayer(slope, {min: 0, max: 60, palette: ['white', 'black']}, 'Slope');

// 8️⃣ Optional export to Google Drive
Export.image.toDrive({
  image: multiYearMeanEVI,
  description: 'Rajasthan_Mean_EVI_2010_2024',
  region: rajasthan,
  scale: 250,
  maxPixels: 1e13
});
