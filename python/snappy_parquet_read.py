""" 
Snippet to read parquet files with snappy compression
"""

from fastparquet import ParquetFile
import snappy
pf = ParquetFile('tst.snappy.parquet')
pf.schema.text    # Check schema
df=pf.to_pandas()
df.head()