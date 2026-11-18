# scripts/preprocess.py
# Cleans the raw USGS and NOAA files and joins them into one table
import os
import numpy as np
import pandas as pd

RAW_DIR = os.path.join("data", "raw")
OUT_DIR = "data"


def parse_date(df):
    """One helper for every date: build a UTC timestamp."""
    if "time" in df.columns:
        return pd.to_datetime(df["time"], utc=True, errors="coerce")
    parts = df[["year", "month", "day", "hour", "minute", "second"]].copy()
    parts[["hour", "minute", "second"]] = parts[["hour", "minute", "second"]].fillna(0)
    return pd.to_datetime(parts, utc=True, errors="coerce")


def haversine_km(lat1, lon1, lat2, lon2):
    """Distance between two points on Earth in km."""
    lat1, lon1, lat2, lon2 = map(np.radians, [lat1, lon1, lat2, lon2])
    a = np.sin((lat2 - lat1) / 2) ** 2 + np.cos(lat1) * np.cos(lat2) * np.sin((lon2 - lon1) / 2) ** 2
    return 6371 * 2 * np.arcsin(np.sqrt(a))


usgs_raw = pd.read_csv(os.path.join(RAW_DIR, "usgs_earthquakes.csv"))
noaa_raw = pd.read_csv(os.path.join(RAW_DIR, "noaa_significant_earthquakes.csv"))

# --- USGS ---
usgs = usgs_raw[usgs_raw["type"] == "earthquake"].copy()
usgs["datetime"] = parse_date(usgs)
usgs = usgs[["id", "datetime", "latitude", "longitude", "depth", "mag", "magType", "place"]]
usgs = usgs.rename(columns={"id": "usgs_id", "depth": "depth_km", "mag": "magnitude"})
usgs = usgs.drop_duplicates(subset="usgs_id")
usgs["year"] = usgs["datetime"].dt.year
print("USGS:", len(usgs_raw), "->", len(usgs), "rows (non-earthquake events removed)")

# --- NOAA ---
noaa = noaa_raw.copy()
noaa["datetime"] = parse_date(noaa)
noaa = noaa.dropna(subset=["datetime", "latitude", "longitude"])
noaa = noaa[["id", "datetime", "country", "locationName", "latitude", "longitude",
             "eqDepth", "eqMagnitude", "deathsTotal", "injuriesTotal",
             "damageMillionsDollarsTotal", "housesDestroyedTotal"]]
noaa = noaa.rename(columns={"id": "noaa_id", "eqDepth": "noaa_depth_km",
                            "eqMagnitude": "noaa_magnitude", "deathsTotal": "deaths",
                            "injuriesTotal": "injuries", "damageMillionsDollarsTotal": "damage_musd",
                            "housesDestroyedTotal": "houses_destroyed"})
noaa = noaa.drop_duplicates(subset="noaa_id")
print("NOAA:", len(noaa_raw), "->", len(noaa), "rows (missing date or location removed)")

# --- Join: for every NOAA event, the USGS event within 100 km that is closest in time (max 1 day) ---
matches = []
for _, ev in noaa.iterrows():
    window = usgs[(usgs["datetime"] - ev["datetime"]).abs() <= pd.Timedelta(days=1)]
    if window.empty:
        matches.append(None)
        continue
    dist = haversine_km(ev["latitude"], ev["longitude"], window["latitude"], window["longitude"])
    window = window[dist <= 100]
    if window.empty:
        matches.append(None)
        continue
    gap = (window["datetime"] - ev["datetime"]).abs()
    matches.append(window.loc[gap.idxmin(), "usgs_id"])
noaa["usgs_id"] = matches

merged = noaa.merge(usgs.drop(columns=["latitude", "longitude"]), on="usgs_id",
                    how="inner", suffixes=("_noaa", ""))

# One NOAA record per USGS earthquake: keep the closest in time (drops aftershocks)
merged["time_gap"] = (merged["datetime"] - merged["datetime_noaa"]).abs()
n_before = len(merged)
merged = merged.sort_values("time_gap").drop_duplicates(subset="usgs_id").sort_index()
merged = merged.drop(columns="time_gap")
print("Removed", n_before - len(merged), "aftershock records matched to the same earthquake")
print("Joined events:", len(merged), "of", len(noaa), "NOAA events")

usgs.to_csv(os.path.join(OUT_DIR, "usgs_clean.csv"), index=False)
merged.to_csv(os.path.join(OUT_DIR, "earthquakes_merged.csv"), index=False)
print("Saved data/usgs_clean.csv and data/earthquakes_merged.csv")
