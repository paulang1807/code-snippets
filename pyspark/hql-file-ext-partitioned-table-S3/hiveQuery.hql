select distinct
cast(id as int) as id,
cast(from_unixtime(unix_timestamp(rpt_month, 'yyyy-MM-dd')) as timestamp) as rpt_month,
-- from {}.sample_table   -- Schema is parsed in the pyspark python file
from {schema}.sample_table    -- Schema is parsed in the pyspark python file