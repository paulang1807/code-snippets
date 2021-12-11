""" 
Snippet to generate data for missing dates in a given dataset
This snippet uses the forward fill method to populate the data for the missing dates

Input Data Sample:
zip	  datekey 	count
4555	20211001	5
94568	20211004	3
4555	20211001	6
94568	20211003	9

Desired Output:
zip	  datekey 	count
04555	20211001	5
04555	20211002	5
04555	20211003	5
04555	20211004	6
04555	20211005	6
94568	20211001	3
94568	20211002	3
94568	20211003	9
94568	20211004	9
94568	20211005	9
"""

import pandas as pd
import numpy as np
import datetime

# Create sample data
df = pd.DataFrame({"zip": pd.Series({"0": 4555, "1": 94568, "2": 4555, "3": 94568}), 
                   "datecode": pd.Series({"0": 20211001, "1": 20211001, "2": 20211004, "3": 20211003}), 
                   "count": pd.Series({"0": 5, "1": 3, "2": 6, "3": 9})})

# Convert date-id and zip to string
df[['zip','datecode']] = df[['zip','datecode']].astype(str)
# US zipcodes are 5 digit long. Left pad the zipcodes to be 5 digit long
df['zip'] = df.zip.str.pad(5,side='left', fillchar='0')

# Get date from date id
df['date_val'] = df.apply(lambda x: x.datecode[:4] + '-' + x.datecode[4:6] + '-' + x.datecode[6:8], axis=1)
df['date_val'] = pd.to_datetime(df['date_val'], format='%Y-%m-%d')

# Group by zip and date
grp_df = df.groupby(['zip','date_val'])[['count']].sum()

# We will reindex by both zip and date
# Create a date range that we can use for reindexing
start=datetime.date(2021,10,1)
end=datetime.date(2021,10,5)
date_range=pd.date_range(start=start, end=end)

# Reindex data
# The 'from_product' will create a cartesian list based on the two params:
#    1. The first index of the group dataframe, which is zip
#    2. The date range created in the previous step
reind_df = grp_df.reindex(pd.MultiIndex.from_product([grp_df.index.levels[0],date_range], names=['r_zip','r_date']), method='ffill')
reind_df.reset_index(inplace=True)

# Save output to csv (dont store dataframe index)
reind_df.to_csv('reindexed_data.csv', index=False)