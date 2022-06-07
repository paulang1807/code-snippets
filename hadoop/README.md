# Code Chunks

### Check if folder exists in hdfs
```bash
hdfs dfs -test -d /data/folder 
if [ $? != 1 ]; then
	echo "folder exists"
fi
# Possible options for -test:
# -d: to check if the directory exists
# -e: to check if the path exists
# -f: to check if the file exists
# -s: to check if the path is not empty
# -z: to check if the file is zero length
```