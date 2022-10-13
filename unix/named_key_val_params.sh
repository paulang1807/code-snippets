#!/bin/bash
# Parse single/multi character named key value parameters

Usage()
{
    printf "\nIncorrect parameters passed. \n
    Single Char Usage: ./named_key_val_params.sh -a=arg1_val -t=arg2_val \n
    Multi Char Usage: ./named_key_val_params.sh --arg1=arg1_val --arg2=arg2_val \n"
    exit -1
}

for i in "$@"  # all arguments passed to the script can be accessed using $@
do
case $i in
    -a=*|--arg1=*)
    ARG1="${i#*=}"   # removes everything upto '=' in the string
    shift # past argument=value
    ;;
    -t=*|--arg2=*)
    ARG2="${i#*=}"
    shift # past argument=value
    ;;
    --default)
    DEFAULT=YES
    shift # past argument with no value
    ;;
    *) 
    Usage >&2   # unknown option
    ;;
esac
done

printf "\nValue of argument 1 is $ARG1 \n"
printf "\nValue of argument 1 is $ARG2 \n"
