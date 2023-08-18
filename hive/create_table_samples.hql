-- Textfile format
CREATE EXTERNAL TABLE IF NOT EXISTS test_table ( 
    column1 bigint 
    ) 
    ROW FORMAT DELIMITED 
    STORED AS Textfile 
    PARTITIONED BY (column1 string) 
    LOCATION 'path'

-- Sequencefile format
CREATE EXTERNAL TABLE IF NOT EXISTS test_table ( 
    column1 bigint 
    )
    ROW FORMAT DELIMITED
    FIELDS TERMINATED BY ‘\001’
    STORED AS Sequencefile

-- JSON format
CREATE EXTERNAL TABLE IF NOT EXISTS test_table (
    column1 INT
    )
    ROW FORMAT SERDE 'org.apache.hive.hcatalog.data.JsonSerDe'
    STORED AS TEXTFILE
    location 'path'

-- Sequencefile clustered by
CREATE EXTERNAL TABLE IF NOT EXISTS test_table ( 
    column1 bigint 
    )
    PARTITIONED BY (partition_column1 VARCHAR(64))
    CLUSTERED BY (cluster_column1) 
    SORTED BY (sort_column1) INTO 32 BUCKETS
    STORED AS Sequencefile

-- Parquet format
CREATE EXTERNAL TABLE IF NOT EXISTS test_table ( 
    column1 bigint 
    )
    ROW FORMAT DELIMITED 
    FIELDS TERMINATED BY ',' 
    STORED as Parquet 
    LOCATION 'path' 
    TBLPROPERTIES ("parquet.compress"="SNAPPY")

-- ORC format
CREATE EXTERNAL TABLE IF NOT EXISTS test_table ( 
    column1 bigint 
    )
    ROW FORMAT DELIMITED 
    FIELDS TERMINATED BY ',' 
    STORED as ORC 
    LOCATION 'path' 
    TBLPROPERTIES ("orc.compress"="SNAPPY")

-- Parquet as select *
CREATE EXTERNAL TABLE IF NOT EXISTS test_table 
    STORED as parquet 
    LOCATION 'path' 
    TBLPROPERTIES ("parquet.compress"="SNAPPY")
AS
SELECT * FROM source_table

-- Nested Struct columns
CREATE TABLE IF NOT EXISTS fin_rpt_stg.dd_oip_metadata(
column1 STRING, 
column2 STRUCT<
  struct_col1:    STRUCT<
    struct_nest1_col1: STRING
    ,struct_nest1_col2:  STRING
    ,struct_nest1_col3:   STRUCT<
      struct_nest2_col1:      STRING
      ,struct_nest2_col2: STRING
      >
    >
  ,struct_col2: STRING
  ,`struct_col1_keyword`: STRING
  >
  )
ROW FORMAT SERDE 'org.apache.hive.hcatalog.data.JsonSerDe'
STORED AS TEXTFILE
location 'path'
;
