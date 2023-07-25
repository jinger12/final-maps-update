import pandas as pd
import statistics
from sklearn.preprocessing import MinMaxScaler
from scipy.stats import zscore


from API_pull_census import df2
from data_fcc import merged_fcc_speeds_2


merged_data = pd.merge(merged_fcc_speeds_2, df2, on='TractID')
print(merged_data)
# Z-score calculations
merged_data['% Over 65 zscore'] = zscore(merged_data['Over 65 pop Percent'])
merged_data['% over 25 with no HS degree zscore'] = zscore(merged_data['Less than HS Grad Percent'])
merged_data['Percent with disability zscore'] = zscore(merged_data['Disabled Percent'])
merged_data['Percent Below Poverty Level zscore'] = zscore(merged_data['Below Poverty Level Percent'])

merged_data['percent NCD zscore'] = zscore(merged_data['percent NCD'])
merged_data['percent NIA zscore'] = zscore(merged_data['percent NIA'])
merged_data['NBBND zscore'] = zscore(merged_data['NBBND'])

# percent NCD

merged_data['median_down_speed zscore'] = zscore(merged_data['DNS_median'])
merged_data['median_up_speed zscore'] = zscore(merged_data['UPS_median'])
# Calculate DDI on census tract level

# Equation 1: INFA Score
merged_data['INFA'] = (0.3 * merged_data['NBBND zscore']) + (0.3 * merged_data['percent NIA zscore']) + (0.3 * merged_data['percent NCD zscore']) - (0.05 * merged_data['median_down_speed zscore']) - (0.05 * merged_data['median_up_speed zscore'])
# Equation 2: SE Score
##MAJOR ISSUE
##FIX

merged_data['SE'] = merged_data['Percent Below Poverty Level zscore'] + merged_data['Percent with disability zscore'] + merged_data['% Over 65 zscore'] + merged_data['% over 25 with no HS degree zscore']
# Equation 3: DDI = INFA + SE
merged_data['DDI'] = merged_data['INFA'] + merged_data['SE']


merged_data['INFA - SE'] = merged_data['INFA'] - merged_data['SE']
scaler = MinMaxScaler(feature_range=(0, 100))

merged_data['DDI scaled'] = scaler.fit_transform(merged_data[['DDI']])
column1 = 'INFA'
column2 = 'SE'
merged_data['INFA - SE'] = merged_data[column1] - merged_data[column2]

merged_data['DDI ratio'] = merged_data['INFA - SE'] / merged_data['DDI']
#rename TractID to GEOID
merged_data = merged_data.rename(columns={'TractID': 'GEOID'})

merged_data.to_csv('data/df_ffc_tract.csv',index=False)
