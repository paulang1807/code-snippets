#!/bin/bash
echo "Start execution ..."

set -e
export LANG=en_US.UTF-8

FatalErrorCheck () {
    if [ $? -ne 0 ]
     then echo "Fatal Error! Exiting"
     exit 1
    fi
}

SCHEMA=$1
TABLE=TABLE1
PARTIONED=True
PARTITION_NAME=rpt_month

echo "loading data to schema $SCHEMA"

echo "\n\n clear out previous data from aws \n  \n" 
aws s3 rm s3://bucketname/$SCHEMA/s3key/ --recursive --exclude "" 
# drop and recreate table - ddl logic should be in createTable.ddl
hive --hivevar schema=$SCHEMA -f createTable.ddl || FatalErrorCheck

# Insert data
SQL_FILE="hiveQuery.hql"
WRITE_MODE='overwrite'
QRY_FILTER=`echo "$SQL_FILE|$SCHEMA|$TABLE|$WRITE_MODE|$PARTIONED|$PARTITION_NAME"`
spark-submit \
--name "SAMPLE_NAME" \
--verbose \
--master yarn --deploy-mode client \
--conf "spark.eventLog.enabled=true" \
hqlFileToExtPartitionedTableS3.py "$QRY_FILTER" || FatalErrorCheck
hive -e "msck repair table $SCHEMA.$TABLE"
hive -e "analyze table $SCHEMA.$TABLE PARTITION ($PARTITION_NAME) compute statistics noscan"

echo "data load complete"  
