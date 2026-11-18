# scripts/download_data.py
# Downloads the raw data from USGS and NOAA into data/raw/
import os
import requests
import pandas as pd

RAW_DIR = os.path.join("data", "raw")
os.makedirs(RAW_DIR, exist_ok=True)

# 1. USGS: all earthquakes of magnitude 6 or larger since 1970 (CSV)
usgs_url = ("https://earthquake.usgs.gov/fdsnws/event/1/query"
            "?format=csv&starttime=1970-01-01&endtime=2025-12-31"
            "&minmagnitude=6&orderby=time-asc")
usgs = pd.read_csv(usgs_url)
usgs.to_csv(os.path.join(RAW_DIR, "usgs_earthquakes.csv"), index=False)
print("USGS:", usgs.shape)

# 2. NOAA: significant earthquakes since 1970 (JSON, page by page)
noaa_url = "https://www.ngdc.noaa.gov/hazel/hazard-service/api/v1/earthquakes"
items, page, total_pages = [], 1, 1
while page <= total_pages:
    r = requests.get(noaa_url, params={"minYear": 1970, "page": page}, timeout=60)
    r.raise_for_status()
    data = r.json()
    items.extend(data["items"])
    total_pages = data["totalPages"]
    page += 1
noaa = pd.DataFrame(items)
noaa.to_csv(os.path.join(RAW_DIR, "noaa_significant_earthquakes.csv"), index=False)
print("NOAA:", noaa.shape)
