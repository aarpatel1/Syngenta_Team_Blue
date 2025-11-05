// ===================================================================
// RAJASTHAN MULTI-YEAR EVI ANALYSIS (2010–2024)
// Compute per-pixel mean, std deviation, and 95% prediction interval
// ===================================================================

// 1️⃣ Load Rajasthan boundary
var states = ee.FeatureCollection("FAO/GAUL/2015/level1");
var rajasthan = states.filter(ee.Filter.eq('ADM1_NAME', 'Rajasthan'));
Map.centerObject(rajasthan, 6);
Map.addLayer(rajasthan, {color: 'blue'}, 'Rajasthan Boundary');

// 2️⃣ Load MODIS MOD13Q1 EVI dataset (16-day composite, 250 m)
var eviCollection = ee.ImageCollection('MODIS/006/MOD13Q1')
  .select('EVI')
  .filterDate('2010-01-01', '2024-12-31')
  .filterBounds(rajasthan);

// 3️⃣ Compute mean EVI per year (so we have 15 yearly means)
var years = ee.List.sequence(2010, 2024);
var yearlyEVI = ee.ImageCollection(
  years.map(function(y) {
    var start = ee.Date.fromYMD(y, 1, 1);
    var end = start.advance(1, 'year');
    var meanYear = eviCollection.filterDate(start, end).mean();
    return meanYear.set('year', y);
  })
);

// 4️⃣ Stack yearly images into one multi-band image
var combined = yearlyEVI.toBands().clip(rajasthan);

// 5️⃣ Compute statistics across the bands (pixelwise)
var stats = combined.reduce(ee.Reducer.mean()
                           .combine(ee.Reducer.stdDev(), null, true))
                    .rename(['Mean', 'StdDev']);

// Compute 95% prediction interval
var lower = stats.select('Mean').subtract(stats.select('StdDev').multiply(1.96)).rename('Lower_95');
var upper = stats.select('Mean').add(stats.select('StdDev').multiply(1.96)).rename('Upper_95');

// Combine into one 4-band image
var eviStats = stats.addBands([lower, upper]).clip(rajasthan);

// 6️⃣ Visualization
Map.addLayer(eviStats.select('Mean'),
             {min: 1500, max: 7000, palette: ['red', 'orange', 'yellow', 'lightgreen', 'green']},
             'Mean EVI (2010–2024)');
Map.addLayer(eviStats.select('StdDev'),
             {min: 0, max: 1000, palette: ['white', 'purple']},
             'EVI StdDev');
Map.addLayer(eviStats.select('Lower_95'),
             {min: 1500, max: 7000, palette: ['red', 'orange', 'yellow', 'lightgreen', 'green']},
             'Lower 95% PI');
Map.addLayer(eviStats.select('Upper_95'),
             {min: 1500, max: 7000, palette: ['red', 'orange', 'yellow', 'lightgreen', 'green']},
             'Upper 95% PI');

// 7️⃣ Export 4-band image as GeoTIFF
Export.image.toDrive({
  image: eviStats,
  description: 'Rajasthan_EVI_Mean_Std_95PI_2010_2024',
  region: rajasthan,
  scale: 250,
  maxPixels: 1e13
});

// 8️⃣ Efficient random pixel sampling (works with continuous data)
var sampled = eviStats.sample({
  region: rajasthan,
  scale: 250,
  numPixels: 20000,   // adjust this value as needed
  geometries: true,
  seed: 42
});

print('Sample size:', sampled.size());


// 9️⃣ Export sample to CSV
Export.table.toDrive({
  collection: sampled,
  description: 'Rajasthan_EVI_MeanStd_95PI_Sample',
  fileFormat: 'CSV'
});



