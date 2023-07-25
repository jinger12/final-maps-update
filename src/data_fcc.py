import pandas as pd
import numpy as np
from API_pull_NIA_NCD import dfz

base = "https://raw.githubusercontent.com/ds5110/rdata/main/fcc/"

# List of files to be read
filenames = [
    "bdc_23_Cable_fixed_broadband_063022.zip",
    "bdc_23_Copper_fixed_broadband_063022.zip",
    "bdc_23_Fiber-to-the-Premises_fixed_broadband_063022.zip",
    "bdc_23_Licensed-Fixed-Wireless_fixed_broadband_063022.zip",
]

def fun(row):
  if (row['max_advertised_download_speed']>=100 and row['max_advertised_upload_speed']>=20):
    return 1
  return 0

# Read and concatenate dataframes
dataframes = [pd.read_csv(base + filename, dtype={'block_fips':str}) for filename in filenames]
df = pd.concat(dataframes, axis=0)

# Drop rows where max_advertised_download_speed is 0
df.drop(df[df.max_advertised_download_speed == 0].index, inplace=True)

# Select the relevant columns and perform the transformations
df['block_fips'] = df['block_fips'].astype(str)
df['block group'] = df['block_fips'].str[0:11]
del df['block_fips']

# Add 'Percent_of_blocks_with_100_20' column
df['Percent_of_blocks_with_100_20'] = df.apply(fun, axis=1)

# Group by block group and calculate median, max, mean, and sum
grouped = df.groupby('block group')
median_download = grouped['max_advertised_download_speed'].median().rename('DNS_median')
median_upload = grouped['max_advertised_upload_speed'].median().rename('UPS_median')
sum_100_20 = grouped['Percent_of_blocks_with_100_20'].mean().rename('Percent_of_blocks_with_100_20')

# Join all series into a single dataframe
df_new = pd.concat([median_download, median_upload, sum_100_20], axis=1).reset_index()

# Add 'Percent_of_blocks_without_100_20' and 'NBBND' columns
df_new['NBBND'] = 1 - df_new['Percent_of_blocks_with_100_20']

# Rename the 'block group' column to 'GEOID' for merging
df_new = df_new.rename(columns={'block group': 'GEOID'})

# Add 'GEOID' column to 'dfz' dataframe for merging
dfz['GEOID'] = dfz['TractID']

# Merge 'df_new' and 'dfz' on 'GEOID'
merged_fcc_speeds_2 = pd.merge(df_new, dfz, on='GEOID', how='left')
#add TractID to merge with other data frames
merged_fcc_speeds_2['TractID'] = merged_fcc_speeds_2['GEOID']
del merged_fcc_speeds_2['GEOID']
print(merged_fcc_speeds_2)
#      DNS_median  UPS_median  Percent_of_blocks_with_100_20     NBBND      TractID  percent NIA  percent NCD
# 0          25.0         3.0                       0.003257  0.996743  23001010100     0.318889     0.224444
# 1          25.0         3.0                       0.000352  0.999648  23001010200     0.053819     0.070733
# 2          25.0         3.0                       0.006860  0.993140  23001010300     0.322314     0.228650
# 3          25.0         3.0                       0.004046  0.995954  23001010400     0.104950     0.110891
# 4          25.0         3.0                       0.002062  0.997938  23001010500     0.133841     0.121872
# ..          ...         ...                            ...       ...          ...          ...          ...
# 395        10.0         1.0                       0.018730  0.981270  23031036003     0.097135     0.097135
# 396        10.0         1.0                       0.013350  0.986650  23031036004     0.076119     0.069146
# 397        25.0         3.0                       0.252963  0.747037  23031037000     0.027612     0.019403
# 398        10.0         1.0                       0.269582  0.730418  23031038001     0.094318     0.124716
# 399        10.0         1.0                       0.325899  0.674101  23031038002     0.044383     0.032594
