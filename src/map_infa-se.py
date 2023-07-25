from data_tract import merged_data

import geopandas as gpd
import matplotlib.pyplot as plt
import requests, zipfile, io
import os
import pandas as pd
import matplotlib as mpl
import numpy as np


# join census_tracts with merged_data_edu on GEOID/FIPS
geo_url = "https://www2.census.gov/geo/tiger/TIGER2022/TRACT/tl_2022_23_tract.zip"
census_tracts_geo = gpd.read_file(geo_url)
census_tracts_geo['GEOID'] = census_tracts_geo['GEOID'].astype(str)
merged_data['GEOID'] = merged_data['GEOID'].astype(str)
# Merge the shapefile with the dataframe
census_tracts_geo_ddi = census_tracts_geo.merge(merged_data, on='GEOID')

# Create a figure and axis object
fig, ax = plt.subplots(figsize=(10,10))

# Plot the census tracts with a light gray color
census_tracts_geo_ddi.plot(ax=ax, color='lightgray')

# Create a colormap
cmap = plt.get_cmap('RdYlGn_r', 10) # Use 10 discrete colors

# Find min and max of the column
min_val = merged_data['INFA - SE'].min()
max_val = merged_data['INFA - SE'].max()

# Generate evenly spaced ticks between min and max
ticks = np.linspace(min_val, max_val, 11)  # 11 ticks, including min and max

# Plot the census tracts again, but this time use the 'INFA - SE scaled' column to color the tracts and apply a color scheme
census_tracts_geo_ddi.plot(ax=ax, column='INFA - SE', legend=True, cmap=cmap,
                           legend_kwds={'ticks': ticks, 'label': 'INFA - SE scaled'})

# Set the title for the plot
plt.title("INFA - SE at Census Tract Level")

# Show the plot
plt.show()

