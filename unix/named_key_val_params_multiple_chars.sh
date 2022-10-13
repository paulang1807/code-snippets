#!/bin/bash
# Parse multi character named key value parameters
# Usage: ./named_key_val_params_multiple_chars.sh arg1=arg1_val arg2=arg2_val

for KEY_VAL_PAIR in "$@"   # all arguments passed to the script can be accessed using $@
do
  printf "\n\n** Key Value pair is $KEY_VAL_PAIR \n"
  set -f; IFS='='
  # Get Key and Value from the Key Value pair string
  set -- $KEY_VAL_PAIR
  KEY=$1; VALUE=$2    
  printf "\nSplit is $KEY, $VALUE \n"
  export "$KEY=$VALUE"
  set +f; unset IFS
done

printf "\n\nArg1 value is $arg1 \n"
printf "\nArg2 value is $arg2 \n"