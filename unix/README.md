# Useful commands

### [Cut](https://en.wikipedia.org/wiki/Cut_(Unix))
```bash
s='one_two_three_four_five'
A="$(cut -d'_' -f2 <<<"$s")"
echo "$A"
# Returns 'two' which is the second field based on '-' as delimiter
```
### [Translate (tr)](https://en.wikipedia.org/wiki/Tr_(Unix))
```bash
# Uppercase to Lowercase
echo "str_to_convert" | tr "[a-z]" "[A-Z]"   
cat FILENAME | tr "[:lower:]" "[:upper:]"

# Translate space to tabs
echo "String with spaces" | tr [:space:] '\t'

# Delete characters
echo "String to modify" | tr -d 'm'  # removes 'm' from the string
echo "string 12345" | tr -d [:digit:] # removes all digits from the string
echo "string 12345" | tr -cd [:digit:] # removes everything except digits

# Find and replace character in a file
tr -s 'CHAR_TO_REPLACE' 'CHAR_TO_REPLACE_WITH' <inputfile >outputfile
```
### [date](https://www.gnu.org/software/coreutils/manual/html_node/date-invocation.html)
```bash
date +"%m-%d-%y"            # 04-03-22
date +"%D"                  # 04/03/22
date +"%T"                  # 14:46:59
echo `$date +"%D %T"`
```

# Code Chunks

### Parse delimited string
```bash
ARR_STR=(${i//-/ })   # i is a string delimited by '-'. eg. test1-test2
Str1=${ARR_STR[0]}
Str2=${ARR_STR[1]}
```
### Check number of parameters passed
```bash
NUM_PARAMS = 3
if [[ "$#" -eq $NUM_PARAMS ]]; then
    # do something
fi
```
### Check for errors
```bash
if [ $? != 0 ];     # if there is error
then
    exit 1          # exit with error code 1
fi
```
### Create folder if not exists
```bash
if [ ! -d "$FOLDERNAME" ]; then   
    mkdir "$FOLDERNAME"
fi

# Alternately, we can use the -p flag to create folder along with all parents that do not exist in a given path
mkdir -p <dir1>/<dir2>/<dir3>
```
### Check if directory is empty
```bash
if [ "$(ls -A $DIRNAME)" ]; then  
    echo "Directory is not empty"
fi
```
### Remove file if it exists
```bash
[ -e ../FILE.txt ] && rm ../FILE.txt
```
### Empty contents of a file
```bash
> file_name.txt
```
### Wait till file is found and then perform some actions
```bash
until [ -f filename.txt ]
do
    sleep 5
done
echo "File Found"
```
### Loop through lines in a file
```bash
for i in $(cat < "$FILENAME"); do
    echo $i
done
```
### Replace in string
```bash
NEW_STR="${OLD_STR//STR_TO_REPLACE/STR_TO_REPLACE_WITH}"
```
### Null check for strings
```bash
# -n checks if string is not null
[ -n "$foo" ] && echo "foo is not null"
# -z checks if string is null (has zero length)
[ -z "$foo" ] && echo "foo is null"
```
### Add date to filename
```bash
NOW=$(date +"%m-%d-%Y")
FILE="filename.$NOW.txt"
echo "test" > $FILE
```
### Manage command dependencies
```bash
# Run second command if first one succeeds
command1 && command2

# Run second command if first one fails
command1 || command2
```

# Useful Settings

```bash
IFS=$'\n'       # make newlines the only separator
set -f          # disable globbing
set -e          # stop script if any command fails
```