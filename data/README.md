# Data card

We use two datasets and join them into one table. Raw files are not committed; `scripts/download_data.py` downloads them again into `data/raw/`.

## Dataset 1: USGS Earthquake Catalog (`usgs_clean.csv`)
- **Source and URL:** U.S. Geological Survey, Earthquake Catalog API, https://earthquake.usgs.gov/fdsnws/event/1/ (CSV)
- **License:** Public domain (U.S. Government work)
- **Date accessed:** 18 November 2026
- **Time range and granularity:** 1970 to 2025, one row per earthquake of magnitude 6 or larger
- **Size:** 7,823 rows x 22 columns (raw); 7,753 rows x 9 columns after cleaning
- **Columns used:** `usgs_id`, `datetime` (UTC), `latitude`, `longitude` (degrees), `depth_km` (km), `magnitude`, `magType` (which magnitude scale was used), `place` (location as text), `year`
- **Known issues:**
  - 70 rows are not earthquakes (for example nuclear explosions).
  - A few depths are negative, which means the event was above sea level.
  - When USGS cannot measure the depth, it often writes a default value: 1,212 earthquakes have exactly 10 km and 898 have exactly 33 km.
  - The number of earthquakes per year jumps around 1983. At first we thought this was better detection, but when we looked at `magType` we saw that the magnitude scale changed: before 1985 most earthquakes were measured with the older mb or Ms scales, after 1985 almost all with Mw. So the years before and after are not fully comparable.
- **Cleaning decisions and why:**
  - We only downloaded magnitude 6+ since 1970, because older and smaller records are incomplete and the API gives at most 20,000 events per request.
  - We converted all dates to UTC so that USGS and NOAA dates can be compared.
  - We removed the non-earthquake events and duplicate ids.
  - We kept the default depths, but we repeated our depth analysis without them (`scripts/eda.ipynb`, cell E12) and the result stayed the same.
- **How to regenerate:** `python scripts/download_data.py && python scripts/preprocess.py`

## Dataset 2: NOAA NCEI Significant Earthquake Database (`noaa_significant_earthquakes.csv`, raw file in `data/raw/`; joined into `earthquakes_merged.csv`)
- **Source and URL:** NOAA National Centers for Environmental Information, Hazel API, https://www.ngdc.noaa.gov/hazel/hazard-service/api/v1/earthquakes (JSON, read page by page); database page: https://www.ncei.noaa.gov/products/natural-hazards/tsunamis-earthquakes-volcanoes/earthquakes
- **License:** Public domain (U.S. Government work)
- **Date accessed:** 18 November 2026
- **Time range and granularity:** 1970 to 2025, one row per significant earthquake (one that caused deaths, damage or a tsunami)
- **Size:** 2,431 rows x 48 columns (raw); still 2,431 rows after cleaning, because no row was missing a date or location
- **Columns used:** `id`, `year`, `month`, `day`, `hour`, `minute`, `second`, `country`, `locationName`, `latitude`, `longitude`, `eqDepth`, `eqMagnitude`, `deathsTotal` (renamed `deaths`), `injuriesTotal`, `damageMillionsDollarsTotal`, `housesDestroyedTotal`
- **Known issues:**
  - Only damaging earthquakes are in this database, so it says nothing about harmless ones.
  - There is no earthquake with 0 deaths. An empty cell can mean "nobody died" or "we don't know".
  - The death numbers are very skewed: in the joined table the median is 9 but the mean is about 2,350, because a few disasters have more than 100,000 deaths.
  - `deathsTotal` also counts deaths from tsunamis, for example most deaths of the 2004 Indian Ocean earthquake.
  - Some numbers are disputed. For Haiti 2010 the government reported 316,000 deaths, but other studies give much lower numbers.
  - Hour, minute or second is sometimes empty.
- **Cleaning decisions and why:**
  - We built one UTC date from the separate date and time columns; if the time was missing we used 00:00.
  - We did **not** replace missing death tolls with 0. If we did, we would be saying that nobody died in earthquakes where we simply don't know, and that would pull the averages down. So all our death analyses only use earthquakes with at least one recorded death.
  - We removed duplicate ids.
- **How to regenerate:** `python scripts/download_data.py && python scripts/preprocess.py`

## Joined table (`earthquakes_merged.csv`)
- **How we joined:** the two datasets have no common id, so for each NOAA earthquake we looked for USGS earthquakes within 1 day and 100 km (haversine distance) and took the one closest in time. Sometimes NOAA lists an aftershock separately and both records matched the same USGS earthquake; in that case we kept the closest one in time, which removed 7 records.
- **Size:** 1,322 rows x 19 columns; 638 of them have at least one recorded death.
- **Unmatched events:** 1,102 NOAA earthquakes found no match. 1,066 of them are smaller than magnitude 6, so they are not in our USGS download anyway; 6 have no magnitude and only 30 (about 1%) are magnitude 6+ without a match.
- **Magnitude and depth:** we use the USGS values, because USGS measures every earthquake in the same way.
- **How to regenerate:** `python scripts/download_data.py && python scripts/preprocess.py`
