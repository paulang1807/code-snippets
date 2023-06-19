# Code snippet showing how to parse named arguments passed to py file
# This example show parsing a string and a list parameter
# Pyhton file will be called using the following command:
# python argparse.py --str1 "strVal" --lst1 "lstVal1,lstVal2"
# In this example str1 is a required parameter whereas lst1 is not


import argparse
import io

if __name__=='__main__':
    # Variables
    parser = argparse.ArgumentParser()
    parser.add_argument("-s", "--str1",type=str, action="store", default=None, required=True, help="String Value")
    parser.add_argument('-t', '--lst1',type=str, action="store", default=None, required=False, help="List of Values")
    args = parser.parse_args()

    print('{} START {}'.format('-'*25, '-'*25))
    str1 = str(args.str1)
    lst1tmp = (str(args.lst1).split(",") if args.lst1 is not None else "")
    # Trim spaces from the strings in the list
    lst1=[x.strip() for x in lst1tmp]

    print('Arguments:')
    print('str1: {}\n'.format(str1))
    print('lst1: {}\n'.format(lst1))



