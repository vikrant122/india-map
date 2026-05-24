import geopandas as gpd
import matplotlib.pyplot as plt
import matplotlib.colors as mcolors
import numpy as np
import requests, io

# ── Census 2011 data ──────────────────────────────────────────────────────────
census = {
    "State": [
        "Andhra Pradesh","Arunachal Pradesh","Assam","Bihar","Chhattisgarh",
        "Goa","Gujarat","Haryana","Himachal Pradesh","Jharkhand","Karnataka",
        "Kerala","Madhya Pradesh","Maharashtra","Manipur","Meghalaya","Mizoram",
        "Nagaland","Odisha","Punjab","Rajasthan","Sikkim","Tamil Nadu",
        "Telangana","Tripura","Uttar Pradesh","Uttarakhand","West Bengal",
        "Jammu and Kashmir","Delhi",
    ],
    "Population": [
        49386799,1383727,31205576,104099452,25545198,1458545,60439692,25351462,
        6864602,32988134,61095297,33406061,72626809,112374333,2855794,2966889,
        1097206,1978502,41974218,27743338,68548437,610577,72147030,35003674,
        3673917,199812341,10086292,91276115,12541302,16787941,
    ],
    "Male": [
        24738820,720232,15939443,54278157,12827915,739140,31491260,13494734,
        3481873,16930315,30966657,16027412,37612306,58243056,1438586,1492668,
        555339,1024649,21212136,14634819,35550997,321661,36137975,17611633,
        1874376,104480510,5137773,46809027,6640662,9005737,
    ],
    "Female": [
        24647979,663495,15266133,49821295,12717283,719405,28948432,11856728,
        3382729,16057819,30128640,17378649,35014503,54131277,1417208,1474221,
        541867,953853,20762082,13108519,32997440,288916,36009055,17392041,
        1799541,95331831,4948519,44467088,5900640,7782204,
    ],
    "Literacy_Rate": [
        74.00,65.38,72.19,61.80,70.28,88.70,78.03,75.55,82.80,66.41,75.60,
        94.00,69.32,82.34,76.94,74.43,91.33,79.55,72.87,75.84,66.11,81.42,
        80.09,66.46,87.22,67.70,78.82,76.26,67.16,86.21,
    ],
}
import pandas as pd
df = pd.DataFrame(census)
df["Illiteracy_Rate"] = 100 - df["Literacy_Rate"]

# ── Load India GeoJSON ────────────────────────────────────────────────────────
url = "https://raw.githubusercontent.com/geohacker/india/master/state/india_state.geojson"
gdf = gpd.read_file(url)
print(gdf.columns)          # check the name column (usually 'NAME_1' or 'ST_NM')
name_col = "NAME_1"         # adjust if needed

gdf = gdf.merge(df, left_on=name_col, right_on="State", how="left")

# ── Plot all 5 categories ─────────────────────────────────────────────────────
categories = {
    "Population":      ("Blues",   "Total Population"),
    "Male":            ("Purples", "Male Population"),
    "Female":          ("RdPu",    "Female Population"),
    "Literacy_Rate":   ("Greens",  "Literacy Rate (%)"),
    "Illiteracy_Rate": ("Oranges", "Illiteracy Rate (%)"),
}

fig, axes = plt.subplots(2, 3, figsize=(20, 14))
axes = axes.flatten()

for i, (col, (cmap, title)) in enumerate(categories.items()):
    ax = axes[i]
    gdf.plot(
        column=col,
        cmap=cmap,
        linewidth=0.5,
        edgecolor="white",
        legend=True,
        legend_kwds={"shrink": 0.6, "label": title},
        missing_kwds={"color": "lightgrey", "label": "No data"},
        ax=ax,
    )
    ax.set_title(title, fontsize=13, fontweight="bold", pad=8)
    ax.axis("off")

axes[-1].axis("off")   # hide the 6th subplot
fig.suptitle("India — Census 2011 Demographics by State", fontsize=16, fontweight="bold", y=1.01)
plt.tight_layout()
plt.savefig("india_census_map.png", dpi=150, bbox_inches="tight")
plt.show()
