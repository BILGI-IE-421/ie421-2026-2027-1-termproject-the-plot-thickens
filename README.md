# IE 421 - Data Science for Engineers Term Project (Please keep this main title in Readme as it is)

## When the Earth Shakes: Understanding Earthquake Patterns
Earthquakes happen all over the world, but their size, depth and human cost differ greatly from place to place. In this project we combine two public datasets: the USGS Earthquake Catalog, which lists every earthquake of magnitude 6 or larger since 1970, and the NOAA NCEI Significant Earthquake Database, which records deaths and damage. We matched the two sources by time and location and obtained 1,322 earthquakes that have both physical measurements and impact data. We ask three questions: where do earthquakes occur most often, and are these the places where they kill the most people; how are magnitude and depth related; and, for earthquakes of similar magnitude, how do death tolls differ by location and depth? Our first results show that magnitude alone explains little of the death toll, so a stronger earthquake is not always a deadlier one. When we compare earthquakes of similar magnitude, shallow earthquakes are clearly deadlier than deep ones, and similar earthquakes have very different consequences in different countries. The final website will tell this story with static, interactive and map-based visualizations and will discuss the limits of the data.

## Student Names
| Name | Student ID |
|---|---|
| Esmanur Çimen | 122203017 |
| Yunus Emre Ayhan | 119203047 |
| Efe Anıl Serin | 122203100 |

## Files
- `data/`: Contains the cleaned USGS catalog (`usgs_clean.csv`, 7,753 earthquakes of magnitude 6+ since 1970) and the joined USGS and NOAA table (`earthquakes_merged.csv`, 1,322 earthquakes with deaths and damage). The full description is in the data card, `data/README.md`. Raw downloads stay in `data/raw/` and are not committed.
- `scripts/`: `download_data.py` downloads the raw data from the USGS and NOAA APIs, `preprocess.py` cleans both datasets and joins them by time and distance, `eda.ipynb` contains our exploratory data analysis, and `figures.py` draws the figures used on the website.
- `visuals/`: `fig1_deaths_vs_magnitude.png` shows deaths against magnitude for every deadly earthquake, and `fig2_deaths_by_depth.png` compares the median death toll of shallow, intermediate and deep earthquakes of similar magnitude.
- `index.html`: Main webpage for GitHub Pages hosting (the styles are inside the file, so there is no separate `css/` folder).
- `PROPOSAL.md`, `AI_USAGE.md`: Our proposal and our AI usage statement.
- `requirements.txt`: Python libraries our scripts need.
- `.github/`: The automatic repository check. Leave it as it is.

## How to run (from the repository root)
```
pip install -r requirements.txt
python scripts/download_data.py
python scripts/preprocess.py
python scripts/figures.py
```

## Key findings
1. Deaths rise only weakly with magnitude: across 638 earthquakes that killed at least one person, Spearman's correlation between magnitude and deaths is only 0.20, and some magnitude 6 earthquakes killed thousands while some above magnitude 8.5 killed only a few.
2. Among earthquakes of magnitude 6.5 to 6.9, the median shallow earthquake (30 km or less) killed 22 people, against 5 for intermediate and 3.5 for deep ones, and the gap remains (16 against 4 and 3.5) when we remove earthquakes whose depth USGS set to a default value.
3. Magnitude and depth are almost unrelated (Spearman's correlation 0.06 across 7,753 earthquakes), so strong earthquakes happen at every depth and depth has to be treated as a separate risk factor.

## Hosting
The project is hosted using GitHub Pages: https://bilgi-ie-421.github.io/ie421-2026-2027-1-termproject-the-plot-thickens/
