# AI usage statement

List every use of an AI assistant (ChatGPT, Claude, Copilot, Gemini, etc.) in this project. Every member must be able to explain all submitted code and figures.

| Date | Tool | Task (what you asked) | Where it is used (file/section) | What you verified and how |
|---|---|---|---|---|
| 2026-11-18 | Claude | Asked which limits to use when downloading the USGS data; Claude suggested magnitude 6+ and events since 1970, because the API returns at most 20,000 events per request | `scripts/download_data.py` | We ran the download in Colab and checked the shapes: USGS (7823, 22), NOAA (2431, 48). |
| 2026-11-18 | Claude | Asked for code to clean both datasets: one UTC date format, removing non-earthquake events, and how to handle missing death tolls (we decided not to fill them with 0) | `scripts/preprocess.py` | We retyped and ran the code and checked the row counts after each step (USGS 7,823 to 7,753; NOAA 2,431). |
| 2026-11-18 | Claude | Asked how to join the two datasets without a common id; Claude suggested matching within 1 day and 100 km (haversine distance) | `scripts/preprocess.py` | We checked the 1,102 unmatched NOAA events: 1,066 have magnitude below 6, so they are not in our USGS download. |
| 2026-11-18 | Claude | Asked Claude to review our code; it found that NOAA aftershocks were matched to the same USGS earthquake and suggested keeping only the match closest in time | `scripts/preprocess.py` | We reran the code and confirmed there are no duplicate ids left (1,322 joined earthquakes). |
| 2026-11-18 | Claude | Asked for EDA code and analysis ideas; Claude suggested the median instead of the mean for skewed death tolls, comparing earthquakes of similar magnitude (6.5 to 6.9), Spearman correlation and a log axis | `scripts/eda.ipynb` | We retyped and ran every cell and checked the tables and plots ourselves. |
| 2026-11-18 | Claude | Asked whether our depth result could come from data problems; Claude suggested repeating the comparison without the default USGS depths (10 and 33 km) | `scripts/eda.ipynb` (cell E12) | We ran it; shallow earthquakes are still the deadliest group (median 16 against 4 and 3.5). |
| 2026-11-18 | Claude | Asked for code for the two figures (titles, colours, labels) | `scripts/figures.py`, `visuals/` | We compared the numbers on the figures with our EDA tables. |
| 2026-11-18 | Claude | Asked for a draft of the data card and the website text | `data/README.md`, `index.html` | We reviewed and edited the text and checked every number against our notebook output. |

Limitations and conclusions will be written in our own words for the final version.
