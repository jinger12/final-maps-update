import pandas as pd

# Gather information for and calculate all SE scores
keys = ['B01001_001E','B01001_020E','B01001_021E','B01001_044E','B01001_045E',
    'B01001_022E','B01001_023E','B01001_046E','B01001_047E','B01001_024E','B01001_025E','B01001_048E',
    'B01001_049E','B17001_002E','B16010_002E','C18108_007E','C18108_008E','C18108_011E','C18108_012E',
    'B28006_002E','B28004_025E','B28004_013E','B28004_009E','B28004_005E']

# construct the url
base = "https://api.census.gov/data/2021/acs/acs5?get="
geog = "&for=tract:*&in=state:23&in=county:*"
url = base + ",".join(keys) + geog
df=pd.read_json(url)

def df_index_reset(df):
  # set the columns from the first row
  df.columns = df.iloc[0]
  # drop the first row
  df.drop(index=0, inplace=True)
  # reset the index
  df.reset_index(drop=True, inplace=True)

df_index_reset(df)
# set the table for integer figures while making the location data strings
df.iloc[:, :-3] = df.iloc[:, :-3].astype(int)
df.iloc[:,-3:] = df.iloc[:,-3:].astype(str)

df.rename(columns = {'B01001_001E':'Total Pop'}, inplace = True)
df.rename(columns = {'B17001_002E':'Below Poverty Level'}, inplace = True)
df.rename(columns = {'B16010_002E':'Less than HS Grad'}, inplace = True)
df.rename(columns = {'B28006_002E':'Less than HS Grad or Equiv'}, inplace = True)
df.rename(columns = {'B28004_025E':'>75K without internet'}, inplace = True)

df['Over 65 pop'] = df.iloc[:, 1:12].sum(axis=1).astype(int)
df['Disabled'] = df.iloc[:, 15:19].sum(axis=1).astype(int)
df['<35K without internet'] = df.iloc[:, 21:24].sum(axis=1).astype(int)
df['TractID'] = df['state']+df['county']+df['tract']

# pulling out the essentials
df2 = df[['TractID', 'Total Pop', 'Over 65 pop', 'Below Poverty Level', 'Less than HS Grad', 'Less than HS Grad or Equiv', 'Disabled', '<35K without internet', '>75K without internet']].copy()
df2[df2.columns[1:]] = df2[df2.columns[1:]].astype(int)

df2 = df2[df2['Total Pop'] != 0]

cols_to_process = ['Over 65 pop', 'Below Poverty Level', 'Disabled','Less than HS Grad']

# Process each column
for col in cols_to_process:
    df2[col + ' Percent'] = df2[col].astype(int) / df2['Total Pop'].astype(int)


# Add '<35K without internet' and '>75K without internet' and divide by 'Total Pop'
df2['Total without internet Percent'] = (df2['<35K without internet'].astype(int) + 
                                           df2['>75K without internet'].astype(int)) / df2['Total Pop'].astype(int)

# Add '<35K without internet' and '>75K without internet' and divide by 'Total Pop'
# df2['Total bellow HS Grad'] = (df2['Less than HS Grad'].astype(int) + 
#                                            df2['Less than HS Grad or Equiv'].astype(int)) / df2['Total Pop'].astype(int)

print(df2.columns)
# 0        TractID  Total Pop  ...  Total without internet Percent  Total bellow HS Grad
# 0    23001010100       1495  ...                        0.154515              0.211371
# 1    23001010200       4643  ...                        0.024553              0.064829
# 2    23001010300       2707  ...                        0.114887              0.102697
# 3    23001010400       2300  ...                        0.032609              0.054783
# 4    23001010500       2123  ...                        0.071126              0.166745
# ..           ...        ...  ...                             ...                   ...
# 401  23031036003       3232  ...                        0.066522              0.025371
# 402  23031036004       4347  ...                        0.008282              0.012882
# 403  23031037000       6725  ...                        0.009219              0.036580
# 404  23031038001       6726  ...                        0.046833              0.045198
# 405  23031038002       3280  ...                        0.017378              0.022866
# Index(['TractID', 'Total Pop', 'Over 65 pop', 'Below Poverty Level',
#        'Less than HS Grad', 'Less than HS Grad or Equiv', 'Disabled',
#        '<35K without internet', '>75K without internet', 'Over 65 pop Percent',
#        'Below Poverty Level Percent', 'Disabled Percent',
#        'Total without internet Percent', 'Total bellow HS Grad'],
#       dtype='object', name=0)
#Less than HS Grad Percent