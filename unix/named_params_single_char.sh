#!/bin/bash
# Parse single character named parameters

Usage()
{
  printf "\nIncorrect parameters passed. \n
  Usage: ./named_params_single_char.sh -a arg1_val -t arg2_val \n"
  exit -1
}

while getopts ":a:t:" opt; do
  case $opt in
    a) ARG1="$OPTARG"
    ;;
    t) ARG2="$OPTARG"
    ;;
    \?) Usage >&2
  esac
done

echo "Value of argument 1 is $ARG1"
echo "Value of argument 1 is $ARG2"