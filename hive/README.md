## Hive Code Chunks

### Create Schema
```sql
create schema <schema_name> location "<path>";
```

### Drop Database
```sql
drop database if exists <schema_name> cascade
```

### Create Table
Use backticks to specify column names to use keywords as column names
```sql
create <external> table
if not exists <schema.table_name>
(
    <col1 name> <col1 datatype>,
    ...
)
location "<path>"
[
    row format delimited 
    fields terminated by <'\001'/','>
    comment 'any text comment'
    partitioned by 
    (
        <partition col1 name> <partition col1 datatype>,
        ...
    ) 
    clustered by (<cluster col name>) sorted by (<sort col name>) into <x> buckets
    stored as [<textfile/sequencefile/parquet>]
    tblproperties ([<"parquet.compress"="SNAPPY" / 
                    "orc.compress"="SNAPPY" /
                    "orc.stripe.size"=67108864); -- 64MBStripes
                    >]) 
    -- For Snappy compression, the value "SNAPPY" needs to be uppercase in definition 
    as select * from source_tablename
]
```

### Get Create Table Statement
```sql
show create table <schema.table_name>
```

### Alter Table
```sql
-- Change column datatype
alter table <schema.table_name> change <col_name> <col_name> <new_type>

-- Change location
alter table <schema.table_name> set location '<path>'

-- Change tablename
alter table <schema.table_name> rename to <new_tablename>

-- Add columns
alter table <schema.table_name> add columns ( <col name> <col datatype> );
```

### Drop Table
```sql
drop table <schema.table_name> purge
```

### Change managed table to external:
```sql
alter table <schema.table_name> set tblproperties('EXTERNAL'='TRUE')
```

### Detailed Table Description
```sql
desc formatted <schema.table_name>
desc extended <schema.table_name>
```

### View Partitions
```sql
show partitions <schema.table_name>
```

### Add Partitions
```sql
alter table <schema.table_name> add partition (<partition_col1='partition_val1',partition_col2='partition_val2'>) location 'partition_path';
```

### Drop Partitions
```sql
alter table <schema.table_name> drop if exists partition (<partition_col1='partition_val1',partition_col2='partition_val2'>)

-- Drop all partitions
alter table <schema.table_name> drop partition (<partition_col1> > '0');
```

### Combine smaller files within a partition
```sql
alter table <schema.table_name> partition (<partition_col1='partition_val1',partition_col2='partition_val2'>) concatenate
```

### Explain Plan
```sql
explain <entire query>
```

### Analyze Table
```sql
analyze table <schema.table_name> compute statistics noscan

-- To analyze stats for all partitions of a partitioned table, specify the partition name without any specific values:
analyze table <schema.table_name> partition (<partition_col>) compute statistics noscan;

```

### MSCK Repair
```sql
msck repair table <schema.table_name>

-- If it fails try setting the msck validation path to 'ignore' first and then run the msck command
set hive.msck.path.validation=ignore;
```

### View all functions / udfs
```sql
show functions
```

### Unlock Table
```sql
unlock table <schema.table_name>
```

### Save hive output to csv
```sql
insert overwrite local directory '/home/temp' 
row format delimited 
fields terminated by ',' 
select books from <schema.table_name>
```

### Run hive commands from command line
```sql
-- Execute query 
hive -e <hive_query>

-- Pass hive configurations and execute query 
hive -hiveconf <config> -e <hive_query>

-- Execute query stored in a file
hive --database <schema_name> -f <hive_query_file_name>

-- Background execution of query stored in a file
nohup hive --database <schema_name> -f <hive_query_file_name> >> log_file_name 2>&1 &
```

#### Pass hive variables and execute query 
```sql
hive --hivevar var_name1="var_val1" --hivevar var_name2="var_val2" -e <hive_query>

hive --hivevar var_date=`hive -e "select current_date"` -e "select * from table where date=${var_date};"
```

## Date Functions
```sql
-- Change a string to Hive Date format 
from_unixtime(UNIX_TIMESTAMP(<date_column_name>,<date format in string>))

-- Get date time from ISO 8601 formatted string "2023-06-08T18:31:00.463616Z"
from_unixtime(unix_timestamp("2023-06-08T18:31:00.463616Z","yyyy-MM-dd'T'HH:mm:ss.SSSSSS'Z'"),'yyyy-MM-dd HH:mm:ss')

-- To get the first day of the month
date_add(<date_column_name>, 1 - day(<date_column_name>) )

-- Get last date of month
last_day(<date_column_name>)

-- Get last day of month (Monday=1, Sunday=7)
date_format(last_day(<date_column_name>), "u")

-- Get last day value in 'yyyy-MM-dd' format from 'month year' (e.g. August 2019) value:
last_day(from_unixtime(unix_timestamp('August 2019','MMM yyyy'),'yyyy-MM-dd'))

-- Add days to a date
date_add(last_day(<date_column_name>), 1)

-- Get first day of last month (Monday=1, Sunday=7)
date_format(date_add(last_day(<date_column_name>), 1), "u")
```

## Useful configs
```sql
-- Allow column names same as reserved keywords:
hive.support.sql11.reserved.keywords=false
```

## Beeline Code Chunks

### Beeline in EC2
```sql
beeline -u "jdbc:hive2://$(hostname):10000/default;principal=hive/$(hostname)@EC2.INTERNAL;saslQop=auth-conf"

beeline -u "jdbc:hive2://$(hostname):10000/default;principal=hive/$(hostname)@EC2.INTERNAL;AuthMech=1;KrbRealm=<REALM_NAME>;KrbHostFQDN=<host FQDN>;KrbServiceName=<hive>"
```

### Connect to database using JDBC from Beeline
```sql
!connect jdbc:hive2://localhost:10000 <username> <password>
```

### Run beeline commands from command line
```sql
-- Background execution of query stored in a file
nohup beeline -u "jdbc:hive2://$(hostname):10000/default;principal=hive/$(hostname)@EC2.INTERNAL" -f <hive_query_file_name> --hivevar var_name="var_val" >> log_file_name 2>&1 &

-- Additional Options
    -- Use --incremental=true to avoid java heap space errors in stdout
    -- Use --outputformat=<csv2> to specify the desired output format
    -- Use --showHeader=false to hide the column headers
    -- Use --silent=true for silent execution
```