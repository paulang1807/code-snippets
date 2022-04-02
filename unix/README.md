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

# Code Chunks

### Parse delimited string
```bash
ARR_STR=(${i//-/ })   # i is a string delimited by '-'. eg. test1-test2
Str1=${ARR_STR[0]}
Str2=${ARR_STR[1]}
```
### Create folder if not exists
```bash
if [ ! -d "$FOLDERNAME" ]; then   
    mkdir "$FOLDERNAME"
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

# Useful Settings

```bash
IFS=$'\n'       # make newlines the only separator
set -f          # disable globbing
```