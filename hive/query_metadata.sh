#!/bin/bash

# Sample script to query hive metadata

# The following script finds all columns of datatype 'timestamp' across all the tables in a given schema

db='db_name_to_explore'
for i in `hive --hivevar db=$db -e 'use {db}; show tables;'`;
do
        for j in $i;
        do
                echo $j >> out.txt
                echo "------" >> out.txt
                eval "hive -e 'describe $db.$j'" >> $j.txt
                # Add pipe delimiter
                sed -i 's/\t/|/g' ./$j.txt   
                # Find rows where the second pipe delimited value is 'timestamp'
                awk -F'|' '$2 ~ "timestamp"' $j.txt >> out.txt  
                echo "" >> out.txt
        done
done
