# Importing pandas package
import pandas as pd
import pandas as pd
import requests
import json
from scipy.stats import zscore
import numpy as np

# QUESTION - SHOULD WE REMOVE ANY AND ALL ACTIVE KEYS?
# Setup variables for API request needed for NIA and NCD scores
MY_KEY = '083b3312e02e0ad2dc088fbed3f8c669097c2e45'

url = 'https://api.census.gov/data/2021/acs/acs5'
params = {
    'get': 'B28002_013E,B11016_001E,B28001_002E,B01003_001E', 
    'for': 'tract:*',
    'in' : 'state:23&in=county:*',
    'key': MY_KEY
}
# Make the API request and parse the response
response = requests.get(url, params=params)
data = json.loads(response.text)

# Creating DataFrame from data
NIANCDdf = pd.DataFrame(data[1:], columns=data[0], dtype=str)

# Renaming the columns
column_rename = {'B28002_013E' : 'Houses NIA', 
                 'B11016_001E' : 'Total Houses', 
                 'B28001_002E' : 'Houses w/ CD', 
                 'B01003_001E' : 'Total Pop', 
                 'block group' : 'group'}

NIANCDdf.rename(columns=column_rename, inplace=True)

# Creating 'tract group' by concatenating 'state', 'county', and 'tract'
NIANCDdf['TractID'] = NIANCDdf.state + NIANCDdf.county + NIANCDdf.tract

# Calculating 'percent NCD' and 'percent NIA'
NIANCDdf['percent NCD'] = 1 - NIANCDdf['Houses w/ CD'].astype(int) / NIANCDdf['Total Houses'].astype(int)
NIANCDdf['percent NIA'] = NIANCDdf['Houses NIA'].astype(int) / NIANCDdf['Total Houses'].astype(int)

# Creating a copy of 'tract group','percent NIA', and 'percent NCD' from NIANCDdf
dfz = NIANCDdf[['TractID','percent NIA','percent NCD']].copy()
print(dfz)

#      TractID  percent NIA  percent NCD
# 0    23001010100     0.318889     0.224444
# 1    23001010200     0.053819     0.070733
# 2    23001010300     0.322314     0.228650
# 3    23001010400     0.104950     0.110891
# 4    23001010500     0.133841     0.121872
# ..           ...          ...          ...
# 402  23031036004     0.076119     0.069146
# 403  23031037000     0.027612     0.019403
# 404  23031038001     0.094318     0.124716
# 405  23031038002     0.044383     0.032594
# 406  23031990100          NaN          NaN