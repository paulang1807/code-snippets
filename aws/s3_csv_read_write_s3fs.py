import s3fs
import pandas as pd

# Read from file
df1 = pd.read_csv('s3://crpfin-oip-prd/temp/oip-meta/oif_meta.csv')

# Write to file
fs = s3fs.S3FileSystem(anon=False)
with fs.open('s3://crpfin-oip-prd/temp/oip-meta/oif_meta_new.csv','w') as f:
    df1.to_csv(f)