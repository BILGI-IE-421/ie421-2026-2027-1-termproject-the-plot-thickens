# scripts/figures.py
# Makes every figure used on the site and saves it in visuals/
import os
import pandas as pd
import matplotlib.pyplot as plt

GREY, INK, ACCENT = "#9a9a9a", "#333333", "#eb6834"
SOURCE = "Source: USGS Earthquake Catalog and NOAA NCEI Significant Earthquake Database, 1970-2025"
plt.rcParams.update({"font.size": 11, "axes.grid": False})
os.makedirs("visuals", exist_ok=True)

eq = pd.read_csv(os.path.join("data", "earthquakes_merged.csv"))
known = eq.dropna(subset=["deaths"]).copy()

# Figure 1: deaths versus magnitude
rho = known["magnitude"].corr(known["deaths"], method="spearman")
fig, ax = plt.subplots(figsize=(9, 5.5))
ax.scatter(known["magnitude"], known["deaths"], s=14, alpha=0.5, color=GREY)
ax.set_yscale("log")
ax.set_xlabel("Magnitude")
ax.set_ylabel("Deaths (log scale)")
for side in ["top", "right"]:
    ax.spines[side].set_visible(False)
ax.set_title("A stronger earthquake is not always a deadlier one",
             loc="left", fontweight="bold", pad=28)
ax.text(0, 1.03, f"Deaths per earthquake that killed at least one person, magnitude 6+, 1970-2025 "
        f"({len(known)} events); Spearman's ρ = {rho:.2f}", transform=ax.transAxes, color=INK, fontsize=10)
ax.text(0, -0.15, SOURCE, transform=ax.transAxes, fontsize=8, color="grey")
fig.savefig(os.path.join("visuals", "fig1_deaths_vs_magnitude.png"), dpi=200, bbox_inches="tight")
plt.close(fig)

# Figure 2: similar magnitude, median deaths by depth
known["depth_group"] = pd.cut(known["depth_km"], bins=[-1, 30, 70, 700],
                              labels=["Shallow\n(≤ 30 km)", "Intermediate\n(30-70 km)", "Deep\n(> 70 km)"])
similar = known[(known["magnitude"] >= 6.5) & (known["magnitude"] < 7.0)]
tab = similar.groupby("depth_group", observed=False)["deaths"].agg(["median", "count"])
colors = [ACCENT if i == 0 else GREY for i in range(len(tab))]
fig, ax = plt.subplots(figsize=(8, 5))
bars = ax.bar(tab.index.astype(str), tab["median"], color=colors, width=0.6)
ax.bar_label(bars, labels=[f"{m:g}  (n = {n})" for m, n in zip(tab["median"], tab["count"])],
             padding=3, color=INK)
for side in ["top", "right", "left"]:
    ax.spines[side].set_visible(False)
ax.set_yticks([])
ax.set_ylim(0, tab["median"].max() * 1.2)
ax.set_title("Among similar earthquakes, shallow ones kill the most",
             loc="left", fontweight="bold", pad=28)
ax.text(0, 1.03, "Median deaths per earthquake, magnitude 6.5 to 6.9, by depth, 1970-2025",
        transform=ax.transAxes, color=INK, fontsize=10)
ax.text(0, -0.2, SOURCE, transform=ax.transAxes, fontsize=8, color="grey")
fig.savefig(os.path.join("visuals", "fig2_deaths_by_depth.png"), dpi=200, bbox_inches="tight")
plt.close(fig)
print("Saved visuals/fig1_deaths_vs_magnitude.png and visuals/fig2_deaths_by_depth.png")
